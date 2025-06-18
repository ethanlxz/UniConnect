from django.urls import path,include
from .views import (StudentRegisterView, StudentLoginView, LecturerRegisterView, LecturerLoginView, SendOTPView, VerifyOTPView, 
                    ResendOTPView, StudentProfileView, LecturerProfileView, LecturerResetPassView, StudentResetPassView)

urlpatterns = [
    #Student urls
    path('student/register/', StudentRegisterView.as_view(), name='student_register'),
    path('student/login/', StudentLoginView.as_view(), name='student_login'),
    path('student/resetPass', StudentResetPassView.as_view(), name='student_resetpass'),
    path('student/profile/<str:username>/', StudentProfileView.as_view(), name='student_profile'),
    #Lecturer urls
    path('lecturer/register/', LecturerRegisterView.as_view(), name='lecturer_register'),
    path('lecturer/login/', LecturerLoginView.as_view(), name='lecturer_login'),
    path('lecturer/resetPass', LecturerResetPassView.as_view(), name='lecturer_resetpass'),
    path('lecturer/profile/<str:username>/', LecturerProfileView.as_view(), name='lecturer_profile'),
    # OTP urls
	path('otp/send', SendOTPView.as_view(), name='send_otp'),
	path('otp/verify',VerifyOTPView.as_view(), name='verify_otp'),
 	path('otp/resend',ResendOTPView.as_view(), name='resend_otp'),
] 
