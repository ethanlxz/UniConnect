from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Class
from .serializers import ClassCreateSerializer
from api.models import LecturerProfile, StudentProfile
from rest_framework import status

# Create your views here.
class CreateClassAPIView(APIView):
    def post(self, request):
        serializer = ClassCreateSerializer(data=request.data)
        if serializer.is_valid():
            lecturer_username = request.headers.get('X-Lecturer-Username')
            if not lecturer_username:
                return Response({'detail': 'Lecturer username header is required.'}, status=400)

            try:
                lecturer = LecturerProfile.objects.get(username=lecturer_username)
            except LecturerProfile.DoesNotExist:
                return Response({'detail': 'Lecturer not found.'}, status=404)

            class_instance = serializer.save(lecturer=lecturer)

            # Increment lecturer's class count
            lecturer.class_count += 1
            lecturer.save()

            return Response({
                "name": class_instance.name,
                "code": class_instance.code
            }, status=201)

        return Response(serializer.errors, status=400)

class JoinClassAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'detail': 'Class code is required.'}, status=400)

        try:
            class_instance = Class.objects.get(code=code)
        except Class.DoesNotExist:
            return Response({'detail': 'Invalid class code.'}, status=404)

        student_username = request.headers.get('X-Student-Username')
        if not student_username:
            return Response({'detail': 'Student username is required.'}, status=400)

        try:
            student = StudentProfile.objects.get(username=student_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student profile not found.'}, status=404)

        if class_instance.students.filter(id=student.id).exists():
            return Response({'detail': 'You have already joined this class.'}, status=200)

        class_instance.students.add(student)

        # Increment student join count
        student.joined_class_count += 1
        student.save()

        return Response({'detail': f"{student.name} successfully joined class '{class_instance.name}'."}, status=200)
    
class EditClassAPIView(APIView):
    def put(self, request):
        class_code = request.data.get('code')
        new_name = request.data.get('name')
        lecturer_username = request.headers.get('X-Lecturer-Username')

        if not class_code or not new_name:
            return Response({'detail': 'Class code and new name are required.'}, status=400)

        if not lecturer_username:
            return Response({'detail': 'Lecturer username is required.'}, status=400)

        try:
            lecturer = LecturerProfile.objects.get(username=lecturer_username)
        except LecturerProfile.DoesNotExist:
            return Response({'detail': 'Lecturer not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code, lecturer=lecturer)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        class_instance.name = new_name
        class_instance.save()

        return Response({'detail': 'Class name updated successfully.'})

class DeleteClassAPIView(APIView):
    def delete(self, request):
        class_code = request.data.get('code')
        lecturer_username = request.headers.get('X-Lecturer-Username')

        if not class_code:
            return Response({'detail': 'Class code is required.'}, status=400)

        if not lecturer_username:
            return Response({'detail': 'Lecturer username is required.'}, status=400)

        try:
            lecturer = LecturerProfile.objects.get(username=lecturer_username)
        except LecturerProfile.DoesNotExist:
            return Response({'detail': 'Lecturer not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code, lecturer=lecturer)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        class_instance.delete()
        return Response({'detail': 'Class deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class RemoveStudentAPIView(APIView):
    def post(self, request):
        class_code = request.data.get('code')
        student_username = request.data.get('student_username')
        lecturer_username = request.headers.get('X-Lecturer-Username')

        if not class_code or not student_username:
            return Response({'detail': 'Class code and student username are required.'}, status=400)
        
        if not lecturer_username:
            return Response({'detail': 'Lecturer username is required.'}, status=400)

        try:
            lecturer = LecturerProfile.objects.get(username=lecturer_username)
        except LecturerProfile.DoesNotExist:
            return Response({'detail': 'Lecturer not found.'}, status=404)

        try:
            class_instance = Class.objects.get(code=class_code, lecturer=lecturer)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        try:
            student = StudentProfile.objects.get(username=student_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        if student not in class_instance.students.all():
            return Response({'detail': 'Student is not enrolled in this class.'}, status=400)

        class_instance.students.remove(student)
        return Response({'detail': 'Student removed successfully.'}, status=200)