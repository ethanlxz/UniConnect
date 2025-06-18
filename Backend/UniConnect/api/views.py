from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .serializers import StudentRegisterSerializer, LecturerRegisterSerializer
from .models import StudentProfile, LecturerProfile, OTP_profile
from rest_framework.parsers import MultiPartParser, FormParser

# for OTP function
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_random_code

# JWT Token
from rest_framework_simplejwt.tokens import RefreshToken

# Password hashing
from django.contrib.auth.hashers import make_password


class StudentRegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]

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

class StudentResetPassView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({"error": "Username and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the student by username
            student = StudentProfile.objects.get(username=username)

            # Update the password securely
            student.password = make_password(new_password)
            student.save()

            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
class LecturerRegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
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
        
class LecturerResetPassView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({"error": "Username and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the lecturer by username
            lecturer = LecturerProfile.objects.get(username=username)

            # Update the password securely
            lecturer.password = make_password(new_password)
            lecturer.save()

            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        except LecturerProfile.DoesNotExist:
            return Response({"error": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND)

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
    
class StudentProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def get(self, request, username):
        try:
            student = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        data = {
            'username': student.username,
            'name': student.name,
            'email': student.email,
            'contact_num': student.contact_num,
            'gender': student.get_gender_display(),
            'major': student.major,
            'photo': request.build_absolute_uri(student.profile_image.url) if student.profile_image else None,
            'bio': student.bio,
            'instagram_id': student.instagram_id or ''
        }

        return Response(data, status=200)

    def patch(self, request, username):
        try:
            student = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        student.name = request.data.get('name', student.name)
        student.email = request.data.get('email', student.email)
        student.contact_num = request.data.get('contact_num', student.contact_num)
        student.major = request.data.get('major', student.major)
        student.bio = request.data.get('bio', student.bio)
        student.gender = request.data.get('gender', student.gender)

        if 'instagram_id' in request.data:
            instagram_id = request.data.get('instagram_id')
            if instagram_id and not instagram_id.startswith('@'):
                return Response({'detail': "Instagram ID must start with '@'."}, status=400)
            student.instagram_id = instagram_id

        if 'profile_image' in request.FILES:
            student.profile_image = request.FILES['profile_image']

        student.save()

        updated_data = {
            'username': student.username,
            'name': student.name,
            'email': student.email,
            'contact_num': student.contact_num,
            'gender': student.get_gender_display(),
            'major': student.major,
            'photo': request.build_absolute_uri(student.profile_image.url) if student.profile_image else None,
            'bio': student.bio,
            'instagram_id': student.instagram_id
        }

        return Response(updated_data, status=200)

    
class LecturerProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def get(self, request, username):
        try:
            lecturer = LecturerProfile.objects.get(username=username)
        except LecturerProfile.DoesNotExist:
            return Response({'detail': 'Lecturer not found.'}, status=404)

        data = {
            'username': lecturer.username,
            'name': lecturer.name,
            'email': lecturer.email,
            'contact_num': lecturer.contact_num,
            'major': lecturer.major,
            'photo': request.build_absolute_uri(lecturer.profile_image.url) if lecturer.profile_image else None,
        }

        return Response(data, status=200)
    
    def put(self, request, username):
        username = request.data.get('username')
        if not username:
            return Response({'detail': 'Username is required in the request body.'}, status=400)

        try:
            lecturer = LecturerProfile.objects.get(username=username)
        except LecturerProfile.DoesNotExist:
            return Response({'detail': 'Lecturer not found.'}, status=404)

        lecturer.name = request.data.get('name', lecturer.name)
        lecturer.email = request.data.get('email', lecturer.email)
        lecturer.contact_num = request.data.get('contact_num', lecturer.contact_num)
        lecturer.major = request.data.get('major', lecturer.major)

        if 'profile_image' in request.FILES:
            lecturer.profile_image = request.FILES['profile_image']

        lecturer.save()

        updated_data = {
            'username': lecturer.username,
            'name': lecturer.name,
            'email': lecturer.email,
            'contact_num': lecturer.contact_num,
            'photo': request.build_absolute_uri(lecturer.profile_image.url) if lecturer.profile_image else None,
            'major': lecturer.major,
        }

        return Response(updated_data, status=200)


