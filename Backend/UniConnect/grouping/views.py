from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, GroupRequest
from classing.models import Class
from api.models import StudentProfile
from django.db.models import Q

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

        # Check if sender or receiver is already in a finalized group for the class
        if Group.objects.filter(class_instance=class_instance, members=sender, is_finalized=True).exists():
            return Response({'detail': 'Sender is already in a finalized group for this class.'}, status=400)
        if Group.objects.filter(class_instance=class_instance, members=receiver, is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group for this class.'}, status=400)

        # Check if there is already a pending request between sender and receiver (in either direction)
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
        action = request.data.get('action')  #true (accept), false (decline)

        if not all([request_id, class_code, current_username]) or not isinstance(action, bool):
            return Response({'detail': 'request_id, class_code, current_username, and a boolean action are required.'}, status=400)

        try:
            group_request = GroupRequest.objects.get(id=request_id)
        except GroupRequest.DoesNotExist:
            return Response({'detail': 'Group request not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found with the given code.'}, status=404)

        sender = group_request.sender
        receiver = group_request.receiver

        if receiver.username != current_username:
            return Response({'detail': 'You are not authorized to respond to this request.'}, status=403)

        if sender not in class_instance.students.all() or receiver not in class_instance.students.all():
            return Response({'detail': 'Sender or receiver is not enrolled in this class.'}, status=400)

        if action is False:
            group_request.delete()
            return Response({'detail': 'Request declined.'})


        if Group.objects.filter(class_instance=class_instance, members=receiver, is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group for this class.'}, status=400)

        group = Group.objects.filter(class_instance=class_instance, members=sender, is_finalized=False).first()

        if not group:
            if Group.objects.filter(class_instance=class_instance).count() >= class_instance.group:
                return Response({'detail': 'Maximum number of groups reached for this class.'}, status=400)
            group = Group.objects.create(class_instance=class_instance)
            group.members.add(sender)

        if Group.objects.filter(class_instance=class_instance, members=receiver, is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group for this class.'}, status=400)

        if group.members.count() >= class_instance.min_group_members:
            return Response({'detail': 'Group is already full.'}, status=400)

        group.members.add(receiver)
        group.save()

        if group.members.count() >= class_instance.min_group_members:
            group.is_finalized = True
            group.save()

        group_request.delete()
        return Response({'detail': 'Request accepted and group updated.'})


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
                'sender_username': req.sender.username,
                'receiver_username': req.receiver.username,
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

        finalized_groups = Group.objects.filter(class_instance=class_instance, is_finalized=True).order_by('id')
        forming_groups = Group.objects.filter(class_instance=class_instance, is_finalized=False).order_by('id')

        def serialize_group(group, label_prefix, index):
            members = list(group.members.all())
            member_names = [m.name for m in members]
            while len(member_names) < min_members:
                member_names.append(None)

            return {
                'group_label': f"{label_prefix} {index + 1}",
                'id': group.id,
                'members': member_names,
                'member_count': len(members),
                'is_finalized': group.is_finalized,
            }

        data = {
            'class_code': class_instance.code,
            'class_name': class_instance.name,
            'min_group_members': min_members,
            'max_groups_allowed': max_groups_allowed,
            'final_groups': [serialize_group(group, "Group", idx) for idx, group in enumerate(finalized_groups)],
            'groups_forming': [serialize_group(group, "Forming Group", idx) for idx, group in enumerate(forming_groups)],
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

        # Fetch groups where this student is a member
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

        if not all([username, class_code, group_id]):
            return Response({'detail': 'username, class_code, and group_id are required.'}, status=400)

        try:
            student = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        try:
            group = Group.objects.get(id=group_id, class_instance=class_instance)
        except Group.DoesNotExist:
            return Response({'detail': 'Group not found in the specified class.'}, status=404)

        if student not in group.members.all():
            return Response({'detail': 'Student is not a member of this group.'}, status=400)

        if group.is_finalized:
            return Response({'detail': 'Cannot leave a finalized group.'}, status=400)

        group.members.remove(student)

        # Delete empty group
        if group.members.count() == 0:
            group.delete()
            return Response({'detail': 'Student left and the group was deleted (no members left).'}, status=200)

        return Response({'detail': 'Student successfully left the group.'}, status=200)