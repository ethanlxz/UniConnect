from django.urls import path
from .views import (SendGroupRequestAPIView, RespondToGroupRequestAPIView, GetGroupRequestsAPIView,ListGroupsAPIView, MyGroupsAPIView, 
                    LeaveGroupAPIView, FinalizeTemporaryGroupAPIView, ChangeLeaderAPIView, DefinalizeGroupAPIView, 
                    ConvertToExistingGroupAPIView, RemoveMemberFromTempGroupAPIView, SendJoinGroupRequestAPIView, 
                    RespondToJoinGroupRequestAPIView, GetJoinRequestsAPIView)

urlpatterns = [
    path('send/', SendGroupRequestAPIView.as_view(), name='send-group-request'),
    path('respond/', RespondToGroupRequestAPIView.as_view(), name='respond-group-request'),
    path('requests/', GetGroupRequestsAPIView.as_view(), name='get-group-requests'),
    path('list/', ListGroupsAPIView.as_view(), name='list-groups'),
    path('myGroups/', MyGroupsAPIView.as_view(), name='my-groups'),
    path('leave/', LeaveGroupAPIView.as_view(), name='leave-group'),
    path('finalTG/', FinalizeTemporaryGroupAPIView.as_view(), name='finalize-temporary-group'),
	path('definalTG/',DefinalizeGroupAPIView.as_view(), name='definalized-temporary-group'),
    path('changeLeader/', ChangeLeaderAPIView.as_view(), name='change-leader'),
    path('api/convert-to-group/', ConvertToExistingGroupAPIView.as_view(), name='convert-to-group'),
    path('removeMember/', RemoveMemberFromTempGroupAPIView.as_view(), name='remove-member-from-temp-group'),
    path('sendJoinRequest/', SendJoinGroupRequestAPIView.as_view(), name='send-join-group-request'),
    path('respondJoinRequest/', RespondToJoinGroupRequestAPIView.as_view(), name='respond-join-group-request'),
    path('joinRequests/', GetJoinRequestsAPIView.as_view(), name='get-join-requests'),
]