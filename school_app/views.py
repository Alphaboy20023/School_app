from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from school_app.serializers import  (ExamSerializer,
                        PaymentSerializer, ReceiptSerializer, 
                        IdentityCardSerializer, ResultSerializer,
                        AnnouncementSerializer, PostSerializer,
                        RepostSerializer, Commentserializer, LectureSerializer,
                        NotificationSerializer, DepartmentSerializer)

from school_app.models import ( Receipt, Result, IdentityCard, CustomUser, Announcement, 
            Post, Repost, Comment, Lecture, UserTypes, Payment, Exam,
            Notification, Department, Course, Calendar, TimeTable)

from accounts_app.models import  Student, CustomUser

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError 

# Create your views here.
        
class DepartmentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Department, pk=pk)
    
    def get(self, request, pk=None, format=None):
        if not (request.user.user_type == UserTypes.LECTURER and not request.user.is_admin and not request.user.is_hod):
            return Response({'error':'You are not authorized to carry out this action'}, status=status.HTTP_403_FORBIDDEN)
        
        if pk:
            department = self.get_object(pk)
            serializer= DepartmentSerializer(department, context={'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            departments = Department.objects.all().order_by('name')
            serializer = DepartmentSerializer(departments, many=True, context={'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not (request.user.is_admin and not request.user.is_hod):
            return Response(
                {'error':'You are not authorized to create departments'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = DepartmentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
           
    
    
class PaymentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = PaymentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        admission_number = request.data.get('admission_number')
        if not admission_number:
            return Response({'error':'admission number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            student=Student.objects.get(admission_number=admission_number)
        except Student.DoesNotExist:
            return Response('invalid admission number', status=status.HTTP_400_BAD_REQUEST)
        
        if (request.user.user_type == UserTypes.LECTURER or request.user.is_admin or request.user.is_hod or request.user.is_staff):
            return Response(
                {"error":"You can not have Payment records. Please login as a student"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        payment = serializer.save(user=request.user, admission_number=student)
        payment.status = 'paid'
        payment.save()
        
        receipt = Receipt(
            payment=payment,
            student_name = f'{student.user.username}',
            admission_number= student.admission_number,
            admin_fee = payment.admin_fee,
            course_fee = payment.course_fee,
            library_fee = payment.library_fee,
            total_amount = payment.total,
            payment_status= payment.status,
            # transaction_id = 
        )
        receipt.save()
        receipt_serializer = ReceiptSerializer(receipt)
        return Response(receipt_serializer.data, status= status.HTTP_201_CREATED)
        
    
    def get(self, request):
    
        admission_number = request.query_params.get('admission_number')
        
        if admission_number:
            payments = Payment.objects.filter(admission_number=admission_number)
        else:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class IdCardView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = IdentityCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        if (request.user.user_type == UserTypes.LECTURER or request.user.is_hod or request.user.is_admin):
            return Response(
                {"error":"You are not authorized to have this ID card. Get a staff ID card instead"},
                status=status.HTTP_403_FORBIDDEN
            )
        user_id = request.query_params.get('id')
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            cards = IdentityCard.objects.filter(user=user)
            serializer = IdentityCardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cards = IdentityCard.objects.all()
            serializer = IdentityCardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    


class ResultView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = ResultSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    
    def get(self, request):
        if request.user.user_type == UserTypes.LECTURER:
            return Response(
                {"error":"Lecturers can not have Result record. Please login as a student"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        result_id = request.query_params.get('id')
        admission_number = request.query_params.get('admission_number')
         
        if result_id:
            try:
                result = Result.objects.get(id=result_id)
                serializer=ResultSerializer(result)
                return Response(serializer.data)
            except Result.DoesNotExist:
                return Response({"error":f'result not found'},
                                status=status.HTTP_404_NOT_FOUND)             
                                                   
        elif admission_number:
            try:
                students = Student.objects.get(admission_number=admission_number)
            except Student.DoesNotExist:
                return Response({"error":"Student with this admission number does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            results = Result.objects.filter(admission_number=students)
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            results = Result.objects.all()
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)
    
    def get_object(self, pk):
        return get_object_or_404(Result, pk=pk)
        
    def delete(self, request, pk, format=None):
        if not (request.user.is_admin or request.user.is_staff or request.user.is_hod):
            return Response(
                {'error':'You are not authorized to delete a Result'}
            )
            
        result = self.get_object(pk)
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class AnnouncementView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        if request.user.user_type != UserTypes.LECTURER and not request.user.is_staff:
            return Response({"error":"You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        serializer = AnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def get(self, request):
        if request.user.user_type != UserTypes.LECTURER and not request.user.is_staff and not request.user.is_admin:
            return Response({"error":"You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        announcements = Announcement.objects.filter()
        serializer = AnnouncementSerializer(announcements, many=True)
        
        return Response(serializer.data)
    
    def get_object(self, pk):
        return get_object_or_404(Announcement, pk=pk)
    
    def delete(self, request, pk, format=None):
        if request.user.user_type != UserTypes.LECTURER and not request.user.is_staff and not request.user.is_admin:
            return Response({"error":"You don't not have permissions to delete an announcment"})
        
        announcement = self.get_object(pk)
        announcement.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class PostView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer= PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def get(self, request):
        post= Post.objects.filter()
        serializer = PostSerializer(post, many=True)
        
        return Response(serializer.data)
    
    
class RepostView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer= RepostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def get(self, request):
        post= Repost.objects.filter()
        serializer = RepostSerializer(post, many=True)
        
        return Response(serializer.data)


class CommentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = Commentserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        comment = Comment.objects.filter()
        seirializer = Commentserializer(comment, many=True)
        
        return Response(seirializer.data)
    
    
    
class LectureView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        if request.user.user_type != UserTypes.LECTURER:
            return Response(
                {"error":"You are not authorized to carry out this action"},
                status = status.HTTP_403_FORBIDDEN
            )
            
        serializer = LectureSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        lectures = Lecture.objects.filter()
        seirializer = LectureSerializer(lectures, many=True, context={'request': request})
        
        return Response(seirializer.data, status=status.HTTP_200_OK)
    
    def get_object(self, pk):
        return get_object_or_404(Lecture, pk=pk)
        
    def delete(self, request, pk, format=None):
        if not (request.user.user_type == UserTypes.LECTURER):
            return Response(
                {'error':'You are not authorized to delete a Lecture'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        lecture = self.get_object(pk)
        lecture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class ExamView(APIView):
    def post(self, request):
        if request.user.user_type != UserTypes.LECTURER and not request.user.is_staff and not request.user.is_admin:
            return Response({"error":"You are not authorized to carry out this action"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ExamSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def get(self, request):
        if request.user.user_type != UserTypes.LECTURER and not request.user.is_staff and not request.user.is_admin:
            return Response({"error":"You are not authorized to carry out this action"}, status=status.HTTP_403_FORBIDDEN)
        exams = Exam.objects.all().order_by('-date')
        serializer = ExamSerializer(exams, many=True, context={'request':request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def get_object(self, pk):
        return get_object_or_404(Exam, pk=pk)
        
    def delete(self, request, pk, format=None):
        if not (request.user.is_admin or request.user.is_staff):
            return Response(
                {'error':'You are not authorized to delete an Exam'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        exam = self.get_object(pk)
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationView(APIView):
    
    def get(self, request):
        notifs = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifs, many=True, context={"request":request} )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = NotificationSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Course, AcademicSession, Calendar, TimeTable