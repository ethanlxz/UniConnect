from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, GroupRequest, TemporaryGroup, JoinGroupRequest
from classing.models import Class
from api.models import StudentProfile
from django.db.models import Q
from django.db.models import Count

# for group conversion
from django.db import transaction 

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
        sender_groups = TemporaryGroup.objects.filter(class_instance=class_instance, members=sender)
        receiver_groups = TemporaryGroup.objects.filter(class_instance=class_instance, members=receiver)

        if sender_groups.filter(id__in=receiver_groups.values_list('id', flat=True)).exists():
            return Response({'detail': 'Sender and receiver are already in the same group.'}, status=400)

        # Check if sender or receiver is already in a finalized TemporaryGroup
        if sender_groups.filter(is_finalized=True).exists():
            return Response({'detail': 'Sender is already in a finalized group for this class.'}, status=400)
        if receiver_groups.filter(is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group for this class.'}, status=400)
        
        # Check if sender or receiver is already in a finalized Group (permanent group)
        if Group.objects.filter(class_instance=class_instance, members=sender).exists():
            return Response({'detail': 'Sender is already in a fixed group for this class.'}, status=400)
        if Group.objects.filter(class_instance=class_instance, members=receiver).exists():
            return Response({'detail': 'Receiver is already in a fixed group for this class.'}, status=400)

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

        if Group.objects.filter(class_instance=class_instance, members=sender).exists():
            return Response({'detail': 'Sender is already in a fixed group for this class.'}, status=400)
        if Group.objects.filter(class_instance=class_instance, members=receiver).exists():
            return Response({'detail': 'Receiver is already in a fixed group for this class.'}, status=400)
        if TemporaryGroup.objects.filter(class_instance=class_instance, members=sender, is_finalized=True).exists():
            return Response({'detail': 'Sender is already in a finalized group.'}, status=400)
        if TemporaryGroup.objects.filter(class_instance=class_instance, members=receiver, is_finalized=True).exists():
            return Response({'detail': 'Receiver is already in a finalized group.'}, status=400)

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
        finalized_groups = Group.objects.filter(class_instance=class_instance).order_by('group_id')

        # Delete all empty temporary groups
        TemporaryGroup.objects.filter(class_instance=class_instance, members__isnull=True).delete()

        # Reload temp groups after deletion
        temp_groups = TemporaryGroup.objects.filter(class_instance=class_instance).annotate(
            member_count=Count('members')
        ).filter(member_count__gt=0).order_by('id')

        def serialize_finalized_group(group, index):
            members = list(group.members.all())
            member_usernames = [m.username for m in members]
            leader_username = group.leader.username if group.leader else "No leader"
    
            return {
                'group_type': 'finalized',
                'group_label': f"Group {group.group_id}",
                'group_id': group.group_id,  # Using the explicit group_id field
                'class_code': group.class_instance.code if group.class_instance else None,
                'members': member_usernames,
                'member_count': group.current_member_count(),  # Using model method
                'max_members': group.max_members,
                'is_full': group.is_full,
                'leader': leader_username,
                'leader_id': group.leader.id if group.leader else None,
            }

        def serialize_temp_group(temp_group, index):
            members = list(temp_group.members.all())
            member_usernames = [m.username for m in members]
            while len(member_usernames) < min_members:
                member_usernames.append(None)
            return {
                'group_type': 'temporary',
                'group_label': f"Temp Group {index + 1}",
                'id': temp_group.id,
                'leader': temp_group.leader.username if temp_group.leader else None,
                'members': member_usernames,
                'member_count': len(members),
                'is_finalized': temp_group.is_finalized,
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

        group_data = []

        # Finalized groups
        finalized_groups = Group.objects.filter(members=student)
        for group in finalized_groups:
            class_instance = group.class_instance
            member_names = list(group.members.values_list('name', flat=True))

            group_data.append({
                'group_id': group.group_id,
                'class_code': class_instance.code,
                'class_name': class_instance.name,
                'members': member_names,
                'leader': group.leader.username if group.leader else None,
                'group_type': 'finalized',
            })

        # Temporary groups
        temp_groups = TemporaryGroup.objects.filter(members=student)
        for temp_group in temp_groups:
            class_instance = temp_group.class_instance
            member_names = list(temp_group.members.values_list('name', flat=True))

            group_data.append({
                'group_id': temp_group.id,
                'class_code': class_instance.code,
                'class_name': class_instance.name,
                'members': member_names,
                'leader': temp_group.leader.username if temp_group.leader else None,
                'group_type': 'temporary',
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
        
        temp_group.is_finalized = True
        temp_group.save()

        return Response({'detail': 'Group finalized.'}, status=200)

class DefinalizeGroupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        class_code = request.data.get('class_code')
        temp_group_id = request.data.get('temp_group_id')

        try:
            student = StudentProfile.objects.get(username=username)
            class_instance = Class.objects.get(code=class_code)
            temp_group = TemporaryGroup.objects.get(
                id=temp_group_id, 
                class_instance=class_instance,
                is_finalized=True 
            )
        except (StudentProfile.DoesNotExist, Class.DoesNotExist, TemporaryGroup.DoesNotExist):
            return Response({'detail': 'Invalid input or group not found.'}, status=404)
        # Check if user is the group leader
        if temp_group.leader != student:
            return Response({'detail': 'Only leader can definalize.'}, status=403)

        temp_group.is_finalized = False
        temp_group.save()

        return Response({
            'detail': 'Group definalized successfully.',
        }, status=200)
        
class ChangeLeaderAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        class_code = request.data.get('class_code')
        temp_group_id = request.data.get('temp_group_id')
        new_leader_username = request.data.get('new_leader_username')
        new_leader_name = request.data.get('new_leader_name')

        if not all([username, class_code, temp_group_id, new_leader_username, new_leader_name]):
            return Response({
                'detail': 'username, class_code, temp_group_id, new_leader_username, and new_leader_name are required.'
            }, status=400)

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

        if new_leader.name != new_leader_name:
            return Response({'detail': 'Provided name does not match the new leader\'s actual name.'}, status=400)

        temp_group.leader = new_leader
        temp_group.save()

        return Response({
            'detail': 'Leader changed successfully.',
            'new_leader': f"{new_leader.username} ({new_leader.name})"
        }, status=200)

    
    from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ConvertToExistingGroupAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        # Get input data
        username = request.data.get('username')
        class_code = request.data.get('class_code')
        temp_group_id = request.data.get('temp_group_id')
        target_group_id = request.data.get('target_group_id')

        # Validate required fields
        if not all([username, class_code, temp_group_id, target_group_id]):
            return Response({'detail': 'Missing required fields.'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get all necessary objects
            student = StudentProfile.objects.get(username=username)
            class_instance = Class.objects.get(code=class_code)
            temp_group = TemporaryGroup.objects.get(
                id=temp_group_id,
                class_instance=class_instance,
                is_finalized=True
            )
            target_group = Group.objects.get(
                group_id=target_group_id,
                class_instance=class_instance
            )
        except (StudentProfile.DoesNotExist, Class.DoesNotExist, 
               TemporaryGroup.DoesNotExist, Group.DoesNotExist):
            return Response({'detail': 'Invalid input data.'}, 
                          status=status.HTTP_404_NOT_FOUND)

        # Authorization check
        if temp_group.leader != student:
            return Response({'detail': 'Only leader can perform this action.'}, 
                          status=status.HTTP_403_FORBIDDEN)

        # Business logic validation
        temp_member_count = temp_group.current_member_count()
        
        if target_group.is_full:
            return Response({'detail': 'Target group is already full.'},
                          status=status.HTTP_400_BAD_REQUEST)
            
        if target_group.max_members != temp_member_count:
            return Response(
                {'detail': f'Target group requires {target_group.max_members} members, but temporary group has {temp_member_count}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if target group has enough capacity
        available_slots = target_group.max_members - target_group.current_member_count()
        if available_slots < temp_member_count:
            return Response(
                {'detail': f'Target group only has {available_slots} available slots but needs {temp_member_count}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform the conversion
        try:
            # Add all members from temp group to target group
            target_group.members.add(*temp_group.members.all())
            
            # Set leader if not already set
            if not target_group.leader:
                target_group.leader = temp_group.leader
                target_group.save()
            
            # Update is_full status
            target_group.update_is_full()
            
            # Delete the temporary group
            temp_group.delete()
            
            return Response({
                'detail': 'Group converted successfully.',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'detail': f'Error during conversion: {str(e)}'},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveMemberFromTempGroupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')  # The current leader
        member_to_remove = request.data.get('member_username')
        class_code = request.data.get('class_code')
        temp_group_id = request.data.get('temp_group_id')

        if not all([username, member_to_remove, class_code, temp_group_id]):
            return Response({'detail': 'username, member_username, class_code, and temp_group_id are required.'}, status=400)

        try:
            leader = StudentProfile.objects.get(username=username)
            member = StudentProfile.objects.get(username=member_to_remove)
            class_instance = Class.objects.get(code=class_code)
            temp_group = TemporaryGroup.objects.get(id=temp_group_id, class_instance=class_instance)
        except (StudentProfile.DoesNotExist, Class.DoesNotExist, TemporaryGroup.DoesNotExist):
            return Response({'detail': 'Invalid user, class, or group.'}, status=404)

        if temp_group.leader != leader:
            return Response({'detail': 'Only the group leader can remove members.'}, status=403)

        if member == leader:
            return Response({'detail': 'Leader cannot remove themselves.'}, status=400)

        if member not in temp_group.members.all():
            return Response({'detail': 'Member is not in this group.'}, status=400)

        temp_group.members.remove(member)

        # If only 1 member remains, delete the group
        if temp_group.current_member_count() <= 1:
            temp_group.delete()
            return Response({'detail': 'Member removed. Group deleted because only 1 member remained.'}, status=200)

        temp_group.save()

        return Response({'detail': f'{member.username} has been removed from the group.'}, status=200)


class SendJoinGroupRequestAPIView(APIView):
    def post(self, request):
        sender_username = request.data.get('sender_username')
        target_username = request.data.get('target_username')  # Could be any member
        class_code = request.data.get('class_code')

        if not all([sender_username, target_username, class_code]):
            return Response({'detail': 'sender_username, target_username, and class_code are required.'}, status=400)

        try:
            class_instance = Class.objects.get(code=class_code)
            sender = StudentProfile.objects.get(username=sender_username)
            target = StudentProfile.objects.get(username=target_username)
        except (Class.DoesNotExist, StudentProfile.DoesNotExist):
            return Response({'detail': 'Invalid class or user.'}, status=404)

        if sender == target:
            return Response({'detail': 'Sender and target cannot be the same.'}, status=400)

        if sender not in class_instance.students.all() or target not in class_instance.students.all():
            return Response({'detail': 'Users are not in the class.'}, status=400)

        # Get temp group of the target member
        temp_group = TemporaryGroup.objects.filter(class_instance=class_instance, members=target, is_finalized=False).first()
        if not temp_group:
            return Response({'detail': 'Target user is not in a temporary group.'}, status=400)

        # Get the actual group leader
        leader = temp_group.leader
        if not leader:
            return Response({'detail': 'This group has no assigned leader.'}, status=400)

        if sender == leader:
            return Response({'detail': 'You cannot send a join request to your own group.'}, status=400)

        if TemporaryGroup.objects.filter(class_instance=class_instance, members=sender).exists():
            return Response({'detail': 'Sender is already in a temporary group.'}, status=400)
        
        # Check if sender is in a fixed group
        if Group.objects.filter(class_instance=class_instance, members=sender).exists():
            return Response({'detail': 'Sender is already in a fixed group.'}, status=400)

        if JoinGroupRequest.objects.filter(sender=sender, receiver=leader).exists():
            return Response({'detail': 'Join request already sent to this group.'}, status=400)

        JoinGroupRequest.objects.create(sender=sender, receiver=leader, temp_group=temp_group)
        return Response({'detail': f'Join request sent to leader {leader.username}.'}, status=201)


class RespondToJoinGroupRequestAPIView(APIView):
    def post(self, request):
        request_id = request.data.get('request_id')
        class_code = request.data.get('class_code')
        leader_username = request.data.get('leader_username')
        action = request.data.get('action')  #true = accept, false = decline

        if not all([request_id, class_code, leader_username]) or not isinstance(action, bool):
            return Response({'detail': 'request_id, class_code, leader_username, and a boolean action are required.'}, status=400)

        try:
            join_request = JoinGroupRequest.objects.get(id=request_id)
        except JoinGroupRequest.DoesNotExist:
            return Response({'detail': 'Join request not found.'}, status=404)

        if join_request.receiver.username != leader_username:
            return Response({'detail': 'You are not authorized to respond to this request.'}, status=403)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        temp_group = join_request.temp_group
        sender = join_request.sender

        # Ensure the temp_group belongs to the given class
        if temp_group.class_instance != class_instance:
            return Response({'detail': 'This join request does not belong to the specified class.'}, status=400)

        if action is False:
            join_request.delete()
            return Response({'detail': 'Join request declined.'}, status=200)

        # Check if sender already in a group
        if TemporaryGroup.objects.filter(class_instance=class_instance, members=sender).exists():
            join_request.delete()
            return Response({'detail': 'Sender is already in another group.'}, status=400)

        # Add sender to the group
        temp_group.members.add(sender)
        temp_group.save()

        # Delete the join request
        join_request.delete()

        return Response({'detail': f'{sender.username} has been added to the group.'}, status=200)

    
class GetJoinRequestsAPIView(APIView):
    def get(self, request):
        leader_username = request.query_params.get('leader_username')
        class_code = request.query_params.get('class_code')

        if not leader_username or not class_code:
            return Response({'detail': 'leader_username and class_code are required.'}, status=400)

        try:
            leader = StudentProfile.objects.get(username=leader_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Leader not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        # Get the leader’s temp group for that class
        temp_group = TemporaryGroup.objects.filter(class_instance=class_instance, leader=leader).first()
        if not temp_group:
            return Response({'detail': 'No group found for this leader in this class.'}, status=404)

        join_requests = JoinGroupRequest.objects.filter(receiver=leader, temp_group=temp_group)

        data = [
            {
                'request_id': req.id,
                'sender_username': req.sender.username
            }
            for req in join_requests
        ]

        return Response(data)