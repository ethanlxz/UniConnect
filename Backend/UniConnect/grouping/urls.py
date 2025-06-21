from django.urls import path
from .views import SendGroupRequestAPIView, RespondToGroupRequestAPIView, GetGroupRequestsAPIView,ListGroupsAPIView, MyGroupsAPIView, LeaveGroupAPIView, FinalizeTemporaryGroupAPIView, ChangeLeaderAPIView

urlpatterns = [
    path('send/', SendGroupRequestAPIView.as_view(), name='send-group-request'),
    path('respond/', RespondToGroupRequestAPIView.as_view(), name='respond-group-request'),
    path('requests/', GetGroupRequestsAPIView.as_view(), name='get-group-requests'),
    path('list/', ListGroupsAPIView.as_view(), name='list-groups'),
    path('myGroups/', MyGroupsAPIView.as_view(), name='my-groups'),
    path('leave/', LeaveGroupAPIView.as_view(), name='leave-group'),
    path('finalTG/', FinalizeTemporaryGroupAPIView.as_view(), name='finalize-temporary-group'),
    path('changeLeader/', ChangeLeaderAPIView.as_view(), name='change-leader'),
]