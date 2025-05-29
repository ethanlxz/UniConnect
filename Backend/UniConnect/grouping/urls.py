from django.urls import path
from .views import SendGroupRequestAPIView, RespondToGroupRequestAPIView, ListGroupsAPIView

urlpatterns = [
    path('send/', SendGroupRequestAPIView.as_view(), name='send-group-request'),
    path('respond/', RespondToGroupRequestAPIView.as_view(), name='respond-group-request'),
    path('list/', ListGroupsAPIView.as_view(), name='list-groups'),
]
