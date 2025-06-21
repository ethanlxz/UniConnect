from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, GroupRequest, TemporaryGroup
from classing.models import Class
from api.models import StudentProfile
from django.db.models import Q
from django.db.models import Count

# Create your views here.
class SendGroupRequestAPIView(APIView):
    def post(self, request):
        class_code = request.data.get('class_code')
        sender_username = request.data.get('sender_username')
        receiver_username = request.data.get('receiver_username')

        if not all([class_code, sender_username, receiver_username]):
            return Response({'detail': 'class_code, sender_username, and receiver_username are required.'}, status=400)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        try:
            sender = StudentProfile.objects.get(username=sender_username)
            receiver = StudentProfile.objects.get(username=receiver_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Sender or receiver username not found.'}, status=404)

        if sender == receiver:
            return Response({'detail': 'Sender and receiver cannot be the same user.'}, status=400)

        if sender not in class_instance.students.all() or receiver not in class_instance.students.all():
            return Response({'detail': 'Sender or receiver not enrolled in this class.'}, status=400)

        # Check if already in same group (any group, not just finalized)
        sender_groups = Group.objects.filter(class_instance=class_instance, members=sender)
        receiver_groups = Group.objects.filter(class_instance=class_instance, members=receiver)

        if sender_groups.filter(id__in=receiver_groups.values_list('id', flat=True)).exists():
            return Response({'detail': 'Sender and receiver are already in the same group.'}, status=400)

        # Check if sender or receiver is already in a finalized group
        if sender_groups.filter(is_finalized=True).exists():
            return Response({'detail': 'Sender is already in a finalized group for this class.'}, status=400)
        if receiver_groups.filter(is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group for this class.'}, status=400)

        #Check for existing request in either direction
        existing_request = GroupRequest.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        ).exists()

        if existing_request:
            return Response({'detail': 'There is already a pending group request between these users.'}, status=400)

        GroupRequest.objects.create(sender=sender, receiver=receiver)
        return Response({'detail': 'Group request sent.'}, status=201)


class RespondToGroupRequestAPIView(APIView):
    def post(self, request):
        request_id = request.data.get('request_id')
        class_code = request.data.get('class_code')
        current_username = request.data.get('current_username')
        action = request.data.get('action')  # true = accept, false = decline

        if not all([request_id, class_code, current_username]) or not isinstance(action, bool):
            return Response({'detail': 'request_id, class_code, current_username, and a boolean action are required.'}, status=400)

        try:
            group_request = GroupRequest.objects.get(id=request_id)
        except GroupRequest.DoesNotExist:
            return Response({'detail': 'Group request not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        sender = group_request.sender
        receiver = group_request.receiver

        if receiver.username != current_username:
            return Response({'detail': 'You are not authorized to respond to this request.'}, status=403)

        if sender not in class_instance.students.all() or receiver not in class_instance.students.all():
            return Response({'detail': 'Sender or receiver not enrolled in this class.'}, status=400)

        if action is False:
            group_request.delete()
            return Response({'detail': 'Request declined.'})

        if Group.objects.filter(class_instance=class_instance, members=receiver, is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group for this class.'}, status=400)

        temp_group = TemporaryGroup.objects.filter(class_instance=class_instance, members=sender).first()

        if not temp_group:
            temp_group = TemporaryGroup.objects.create(
                class_instance=class_instance,
                leader=sender
            )
            temp_group.members.add(sender)

        old_group = TemporaryGroup.objects.filter(class_instance=class_instance, members=receiver).exclude(id=temp_group.id).first()
        if old_group:
            old_group.members.remove(receiver)
            if old_group.members.count() <= 1:
                old_group.members.clear()
                old_group.leader = None
                old_group.save()

        if receiver not in temp_group.members.all():
            temp_group.members.add(receiver)

        temp_group.save()
        group_request.delete()

        return Response({'detail': 'Request accepted. Students added to sender’s temporary group.', 'temp_group_id': temp_group.id}, status=200)


class GetGroupRequestsAPIView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        class_code = request.query_params.get('class_code')

        if not username or not class_code:
            return Response({'detail': 'username and class_code are required.'}, status=400)

        try:
            user = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        if user not in class_instance.students.all():
            return Response({'detail': 'User not enrolled in this class.'}, status=400)

        requests = GroupRequest.objects.filter(receiver=user)
        data = [
            {
                'request_id': req.id,
                'sender_username': req.sender.username
            }
            for req in requests
        ]

        return Response(data)


class ListGroupsAPIView(APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({'detail': 'Class ID is required as a query parameter.'}, status=400)

        try:
            class_instance = Class.objects.get(class_id=class_id)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        min_members = class_instance.min_group_members or 4
        max_groups_allowed = class_instance.group

        # Finalized Groups
        finalized_groups = Group.objects.filter(class_instance=class_instance, is_finalized=True).order_by('id')

        # Delete all empty temporary groups
        TemporaryGroup.objects.filter(class_instance=class_instance, members__isnull=True).delete()

        # Reload temp groups after deletion
        temp_groups = TemporaryGroup.objects.filter(class_instance=class_instance).annotate(
            member_count=Count('members')
        ).filter(member_count__gt=0).order_by('id')

        def serialize_finalized_group(group, index):
            members = list(group.members.all())
            member_names = [m.name for m in members]
            while len(member_names) < min_members:
                member_names.append(None)
            return {
                'group_type': 'finalized',
                'group_label': f"Finalized Group {index + 1}",
                'id': group.id,
                'members': member_names,
                'member_count': len(members),
                'is_finalized': True,
            }

        def serialize_temp_group(temp_group, index):
            members = list(temp_group.members.all())
            member_names = [m.name for m in members]
            while len(member_names) < min_members:
                member_names.append(None)
            return {
                'group_type': 'temporary',
                'group_label': f"Temp Group {index + 1}",
                'id': temp_group.id,
                'leader': temp_group.leader.username if temp_group.leader else None,
                'members': member_names,
                'member_count': len(members),
                'is_finalized': False,
            }

        data = {
            'class_code': class_instance.code,
            'class_name': class_instance.name,
            'min_group_members': min_members,
            'max_groups_allowed': max_groups_allowed,
            'final_groups': [serialize_finalized_group(g, i) for i, g in enumerate(finalized_groups)],
            'temporary_groups': [serialize_temp_group(g, i) for i, g in enumerate(temp_groups)],
        }

        return Response(data, status=200)


class MyGroupsAPIView(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response({'detail': 'Username is required as a query parameter.'}, status=400)

        try:
            student = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        groups = Group.objects.filter(members=student)

        group_data = []
        for group in groups:
            class_instance = group.class_instance
            member_names = list(group.members.values_list('name', flat=True))

            group_data.append({
                'group_id': group.id,
                'class_code': class_instance.code,
                'class_name': class_instance.name,
                'members': member_names,
                'is_finalized': group.is_finalized,
            })

        return Response({'groups': group_data}, status=200)
    
class LeaveGroupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        class_code = request.data.get('class_code')
        group_id = request.data.get('group_id')
        group_type = request.data.get('group_type')  # 'temporary' or 'finalized'

        if not all([username, class_code, group_id, group_type]):
            return Response({'detail': 'username, class_code, group_id, and group_type are required.'}, status=400)

        try:
            student = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        if group_type == 'temporary':
            try:
                temp_group = TemporaryGroup.objects.get(id=group_id, class_instance=class_instance)
            except TemporaryGroup.DoesNotExist:
                return Response({'detail': 'Temporary group not found.'}, status=404)

            if student not in temp_group.members.all():
                return Response({'detail': 'Student is not a member of this temporary group.'}, status=400)

            temp_group.members.remove(student)

            if temp_group.current_member_count() <= 1:
                temp_group.delete()
                return Response({'detail': 'Student left. Temporary group deleted because only 1 member remained.'}, status=200)
            
            if temp_group.leader == student:
                remaining_members = list(temp_group.members.all())
                temp_group.leader = remaining_members[0] if remaining_members else None
            temp_group.save()

            return Response({'detail': 'Student successfully left the temporary group.'}, status=200)

        elif group_type == 'finalized':
            try:
                final_group = Group.objects.get(id=group_id, class_instance=class_instance, is_finalized=True)
            except Group.DoesNotExist:
                return Response({'detail': 'Finalized group not found.'}, status=404)

            if student not in final_group.members.all():
                return Response({'detail': 'Student is not a member of this finalized group.'}, status=400)

            return Response({'detail': 'Cannot leave a finalized group.'}, status=400)

        else:
            return Response({'detail': 'Invalid group type. Must be "temporary" or "finalized".'}, status=400)
    

class FinalizeTemporaryGroupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        class_code = request.data.get('class_code')
        temp_group_id = request.data.get('temp_group_id')

        try:
            student = StudentProfile.objects.get(username=username)
            class_instance = Class.objects.get(code=class_code)
            temp_group = TemporaryGroup.objects.get(id=temp_group_id, class_instance=class_instance)
        except (StudentProfile.DoesNotExist, Class.DoesNotExist, TemporaryGroup.DoesNotExist):
            return Response({'detail': 'Invalid input.'}, status=404)

        if temp_group.leader != student:
            return Response({'detail': 'Only leader can finalize.'}, status=403)

        if temp_group.current_member_count() < class_instance.min_group_members:
            return Response({'detail': 'Not enough members to finalize.'}, status=400)

        final_group = Group.objects.create(class_instance=class_instance, is_finalized=True)
        final_group.members.set(temp_group.members.all())

        temp_group.delete()

        return Response({'detail': 'Group finalized.'}, status=200)

class ChangeLeaderAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        class_code = request.data.get('class_code')
        temp_group_id = request.data.get('temp_group_id')
        new_leader_username = request.data.get('new_leader_username')

        if not all([username, class_code, temp_group_id, new_leader_username]):
            return Response({'detail': 'username, class_code, temp_group_id, and new_leader_username are required.'}, status=400)

        try:
            current_leader = StudentProfile.objects.get(username=username)
            new_leader = StudentProfile.objects.get(username=new_leader_username)
            class_instance = Class.objects.get(code=class_code)
            temp_group = TemporaryGroup.objects.get(id=temp_group_id, class_instance=class_instance)
        except (StudentProfile.DoesNotExist, Class.DoesNotExist, TemporaryGroup.DoesNotExist):
            return Response({'detail': 'Invalid username, class code, or group ID.'}, status=404)

        if temp_group.leader != current_leader:
            return Response({'detail': 'Only the current leader can change the leader.'}, status=403)

        if new_leader not in temp_group.members.all():
            return Response({'detail': 'New leader must be a member of the group.'}, status=400)

        temp_group.leader = new_leader
        temp_group.save()

        return Response({'detail': f'Leader changed to {new_leader.username} successfully.'}, status=200)