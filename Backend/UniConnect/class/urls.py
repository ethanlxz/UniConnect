from django.urls import path
from .views import CreateClassAPIView, JoinClassAPIView, EditClassAPIView, DeleteClassAPIView, RemoveStudentAPIView

urlpatterns = [
    path('create/', CreateClassAPIView.as_view(), name='create_class'),
    path('join/', JoinClassAPIView.as_view(), name='join_class'),
    path('edit/', EditClassAPIView.as_view(), name='edit_class'),
    path('delete/', DeleteClassAPIView.as_view(), name='delete_class'),
    path('removeStudent/', RemoveStudentAPIView.as_view(), name='remove_student'),
]