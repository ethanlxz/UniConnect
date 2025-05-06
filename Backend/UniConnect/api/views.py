from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .serializers import StudentRegisterSerializer, LecturerRegisterSerializer
from .models import StudentProfile, LecturerProfile

# Create your views here.
class StudentRegisterView(APIView):
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            student = StudentProfile.objects.get(email=email)
            if check_password(password, student.password):
                return Response({"message": "Login successful"})
            else:
                return Response({"error": "Invalid password"}, status=400)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        
class LecturerRegisterView(APIView):
    def post(self, request):
        serializer = LecturerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Lecturer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LecturerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            lecturer = LecturerProfile.objects.get(email=email)
            if check_password(password, lecturer.password):
                return Response({"message": "Login successful"})
            else:
                return Response({"error": "Invalid password"}, status=400)
        except LecturerProfile.DoesNotExist:
            return Response({"error": "Lecturer not found"}, status=404)