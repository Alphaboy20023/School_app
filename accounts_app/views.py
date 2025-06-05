from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts_app.serializers import  ( UserSerializer, StudentSerializer,  LecturerSerializer, LoginSerializer)
from accounts_app.models import  UserTypes
from accounts_app.models import LecturerProfile, Student
from django.contrib.auth import authenticate

# Create your views here.

class RegisterView(APIView):
    
    def post(self, request):
        serializer = UserSerializer (data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {"message": "User has been created successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED
)
    
    
class LoginView(APIView):
    def post(self, request):
        serializer= LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user= serializer.validated_data['user']
            refresh=RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user_id':user.id,
                "username":user.username,
                "email":user.email,
                "user_type":user.user_type
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    
    
class StudentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        if request.user.user_type != UserTypes.STUDENT:
            return Response({"error":"You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def get(self,request):
        user_id = request.query_params.get('id')
        if user_id:
            student = get_object_or_404(Student, user_id=user_id)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        
        
        
class lecturerView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post (self, request):
        if request.user.user_type != UserTypes.LECTURER:
            return Response({"error":"You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        serializer = LecturerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def get (self, request):
        lecturer_id = request.query_params.get('Id')
        if lecturer_id:
            lecturer = get_object_or_404(LecturerProfile, lecturer_id=lecturer_id)
            serializer = LecturerSerializer(lecturer)
            return Response(serializer.data)
        else:
            lecturers = LecturerProfile.objects.all()
            serializer = LecturerSerializer(lecturers, many=True)
            return Response(serializer.data)
        