from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .serializers import StudentRegisterSerializer, LecturerRegisterSerializer
from .models import StudentProfile, LecturerProfile, OTP_profile

# for OTP function
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_random_code

# JWT Token
from rest_framework_simplejwt.tokens import RefreshToken


class StudentRegisterView(APIView):
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Retrieve the student by username
            student = StudentProfile.objects.get(username=username)

            # Check the password
            if check_password(password, student.password):
                # Generate JWT tokens
                refresh = RefreshToken.for_user(student)

                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        
class LecturerRegisterView(APIView):
    def post(self, request):
        serializer = LecturerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Lecturer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LecturerLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Retrieve the lecturer by username
            lecturer = LecturerProfile.objects.get(username=username)

            # Check the password
            if check_password(password, lecturer.password):
                # Generate JWT tokens
                refresh = RefreshToken.for_user(lecturer)

                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except LecturerProfile.DoesNotExist:
            return Response({"error": "Lecturer not found"}, status=status.HTTP_404_NOT_FOUND)

class SendOTPView(APIView):
    
    def sendOTP(self, email):
        
        try:
            otp_profile = OTP_profile.objects.get(email=email)
            
            # If an OTP exists, return a message saying the OTP has already been sent
            if otp_profile.expriarationDate > now():
                return Response({"message": "OTP has already been sent to this email."}, status=status.HTTP_200_OK)
        except OTP_profile.DoesNotExist:
            pass  # If no OTP exists, proceed to generate and send a new OTP
        
        # Generate a random OTP code
        otp_code = generate_random_code()

        # Calculate the expiration date (10 minutes from now)
        expiration_date = now() + timedelta(minutes=10)

        # Store the OTP and expiration in the database
        OTP_profile.objects.update_or_create(
            email=email,
            defaults={
                "code": otp_code,
                "expriarationDate": expiration_date,
            }
        )

        # Send the OTP via email
        subject = "Your OTP Code"
        message = f"Your OTP code is: {otp_code}. It will expire in 10 minutes."
        from_email = "your_email@example.com"
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to send OTP. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the instance method correctly
        return self.sendOTP(email)

class VerifyOTPView(APIView):
    def verify_otp(self, email, otp_code):
        try:
            # Fetch the OTP profile for the given email
            otp_profile = OTP_profile.objects.get(email=email)

            # Check if the OTP has expired
            if now() > otp_profile.expriarationDate:
                return Response({"error": "The OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided OTP matches the stored OTP
            if otp_profile.code == otp_code:
                otp_profile.delete()
                return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        except OTP_profile.DoesNotExist:
            return Response({"error": "No OTP found for the provided email."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("code")

        # Ensure email and OTP are provided
        if not email or not otp_code:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the OTP
        return self.verify_otp(email, otp_code)
    

class ResendOTPView(APIView):
    
    def resendOTP(self, email):
        # First, find the existing OTP for the provided email
        try:
            otp_profile = OTP_profile.objects.get(email=email)

            # Delete the existing OTP
            otp_profile.delete()
        except OTP_profile.DoesNotExist:
            pass  # No existing OTP, proceed to generating a new one

        # Generate a new OTP code
        otp_code = generate_random_code()

        # Calculate the expiration date (10 minutes from now)
        expiration_date = now() + timedelta(minutes=10)

        # Store the new OTP and expiration in the database
        OTP_profile.objects.create(
            email=email,
            code=otp_code,
            expriarationDate=expiration_date,
        )

        # Send the new OTP via email
        subject = "Your New OTP Code"
        message = f"Your new OTP code is: {otp_code}. It will expire in 10 minutes."
        from_email = "your_email@example.com"
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "New OTP sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to send OTP. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the instance method to resend the OTP
        return self.resendOTP(email)
