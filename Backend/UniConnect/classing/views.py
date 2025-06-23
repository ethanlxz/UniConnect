from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Class
from .serializers import ClassCreateSerializer
from api.models import LecturerProfile, StudentProfile
from rest_framework import status
from grouping.models import Group, TemporaryGroup

# Create your views here.


class CreateClassAPIView(APIView):
    def post(self, request):
        serializer = ClassCreateSerializer(data=request.data)
        if serializer.is_valid():
            lecturer_username = request.data.get('username')
            if not lecturer_username:
                return Response({'detail': 'Lecturer username header is required.'}, status=400)

            try:
                lecturer = LecturerProfile.objects.get(username=lecturer_username)
            except LecturerProfile.DoesNotExist:
                return Response({'detail': 'Lecturer not found.'}, status=404)

            validated_data = serializer.validated_data
            max_students = validated_data['max_students']
            num_groups = validated_data['group']
            min_members = validated_data['min_group_members']
            
            base_size = max_students // num_groups
            remainder = max_students % num_groups
            
            class_instance = serializer.save(lecturer=lecturer)
            
            for i in range(num_groups):
                group_size = base_size + 1 if i < remainder else base_size
                
                final_size = max(group_size, min_members)
                
                Group.objects.create(
                    class_instance=class_instance,
                    max_members=final_size
                )

            return Response({
                "name": class_instance.name,
                "code": class_instance.code,
                "max_students": class_instance.max_students,
                "group": class_instance.group,
                "min_group_members": class_instance.min_group_members,
                "created_groups": num_groups
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

        student_username = request.data.get('username')
        if not student_username:
            return Response({'detail': 'Student username is required.'}, status=400)

        try:
            student = StudentProfile.objects.get(username=student_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student profile not found.'}, status=404)
        
        if class_instance.students.count() >= class_instance.max_students:
            return Response({'detail': 'Class is full.'}, status=400)

        if class_instance.students.filter(id=student.id).exists():
            return Response({'detail': 'You have already joined this class.'}, status=200)

        class_instance.students.add(student)

        return Response({'detail': f"{student.name} successfully joined class '{class_instance.name}'."}, status=200)
    
class EditClassAPIView(APIView):
    def put(self, request):
        class_code = request.data.get('code')
        new_name = request.data.get('name')
        lecturer_username = request.data.get('username')

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
        lecturer_username = request.data.get('username')

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
        lecturer_username = request.data.get('username')

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
    
class LecturerClassListAPIView(APIView):
    def post(self, request):
        lecturer_username = request.data.get('username')
        if not lecturer_username:
            return Response({'detail': 'Lecturer username is required.'}, status=400)

        try:
            lecturer = LecturerProfile.objects.get(username=lecturer_username)
        except LecturerProfile.DoesNotExist:
            return Response({'detail': 'Lecturer not found.'}, status=404)

        classes = Class.objects.filter(lecturer=lecturer)
        data = [{"id": c.class_id, "name": c.name, "code": c.code} for c in classes]
        return Response(data, status=200)


class StudentClassListAPIView(APIView):
    def post(self, request):
        student_username = request.data.get('username')
        if not student_username:
            return Response({'detail': 'Student username is required.'}, status=400)

        try:
            student = StudentProfile.objects.get(username=student_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        classes = student.joined_classes.all()
        data = [{"id": c.class_id, "name": c.name, "code": c.code} for c in classes]
        return Response(data, status=200)

class ClassDetailAPIView(APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({'detail': 'Class ID is required as a query parameter.'}, status=400)

        try:
            class_instance = Class.objects.get(class_id=class_id)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        data = {
            'class_id': class_instance.class_id,
            'name': class_instance.name,
            'code': class_instance.code,
            'max_students': class_instance.max_students,
            'current_student_count': class_instance.current_student_count(),
            'group': class_instance.group,
            'min_group_members': class_instance.min_group_members,
            'lecturer': {
                'id': class_instance.lecturer.id,
                'username': class_instance.lecturer.username,
                'name': class_instance.lecturer.name,
                'email': class_instance.lecturer.email,
                'contact_num': class_instance.lecturer.contact_num
            },
            'students': [
                {
                    'id': s.id,
                    'username': s.username,
                    'name': s.name,
                    'email': s.email,
                    'contact_num': s.contact_num
                }
                for s in class_instance.students.all()
            ]
        }

        return Response(data, status=200)
    
class LeaveClassAPIView(APIView):
    def post(self, request):
        class_code = request.data.get('code')
        student_username = request.data.get('username')

        if not class_code or not student_username:
            return Response({'detail': 'Class code and student username are required.'}, status=400)

        try:
            class_instance = Class.objects.get(code=class_code)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        try:
            student = StudentProfile.objects.get(username=student_username)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=404)

        if student not in class_instance.students.all():
            return Response({'detail': 'Student is not enrolled in this class.'}, status=400)
        
        # Check for membership in any TemporaryGroup
        if TemporaryGroup.objects.filter(class_instance=class_instance, members=student).exists():
            return Response({'detail': 'You are in a temporary group. Leave the group before leaving the class.'}, status=400)

        # Check for membership in any Group (finalized or not)
        if Group.objects.filter(class_instance=class_instance, members=student).exists():
            return Response({'detail': 'You are in a group. Leave the group before leaving the class.'}, status=400)

        class_instance.students.remove(student)

        return Response({'detail': 'Successfully left the class.'}, status=200)