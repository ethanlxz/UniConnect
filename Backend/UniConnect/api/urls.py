from django.urls import path
from .views import StudentRegisterView, StudentLoginView, LecturerRegisterView, LecturerLoginView

urlpatterns = [
    path('student/register/', StudentRegisterView.as_view(), name='student_register'),
    path('student/login/', StudentLoginView.as_view(), name='student_login'),
    path('lecturer/register/', LecturerRegisterView.as_view(), name='lecturer_register'),
    path('lecturer/login/', LecturerLoginView.as_view(), name='lecturer_login'),
]
