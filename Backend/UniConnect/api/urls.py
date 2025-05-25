from django.urls import path
from .views import StudentRegisterView, StudentLoginView, LecturerRegisterView, LecturerLoginView, SendOTPView, VerifyOTPView, ResendOTPView, StudentProfileView, LecturerProfileView

urlpatterns = [
    path('student/register/', StudentRegisterView.as_view(), name='student_register'),
    path('student/login/', StudentLoginView.as_view(), name='student_login'),
    path('lecturer/register/', LecturerRegisterView.as_view(), name='lecturer_register'),
    path('lecturer/login/', LecturerLoginView.as_view(), name='lecturer_login'),
	path('otp/send', SendOTPView.as_view(), name='send_otp'),
	path('otp/verify',VerifyOTPView.as_view(), name='verify_otp'),
 	path('otp/resend',ResendOTPView.as_view(), name='resend_otp'),
    path('student/profile/', StudentProfileView.as_view(), name='student_profile'),
    path('lecturer/profile/', LecturerProfileView.as_view(), name='lecturer_profile'),
]
