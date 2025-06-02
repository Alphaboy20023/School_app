
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from school_app.models import (Payment,
    Receipt, IdentityCard, Result, Course, 
    Announcement, Post, Repost, 
    Comment, Lecture, Question, Exam, Notification, 
    Department, AcademicSession, Calendar, TimeTable )

from accounts_app.models import CustomUser, Student
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction

    
class DepartmentSerializer(serializers.ModelSerializer):
    
    hod = serializers.StringRelatedField(read_only=True)
    hod_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(is_hod=True),
        source ='hod', write_only=True, required= False, allow_null=True,
        error_messages={"Does not exist":"HOD wit ID does not exist"}
    )
    
    class Meta:
        model = Department
        fields = ['name', 'dept_code', 'faculty', 'hod', 'hod_id']
        read_only_fields = ['hod']
        
    def create(self, validated_data):
        department = Department.objects.create(**validated_data)
        department.save()
        return department

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        representation.pop('hod_id', None)
        return representation

    


class PaymentSerializer(serializers.ModelSerializer):
    admission_number = serializers.SlugRelatedField(
        queryset= Student.objects.all(),
        slug_field='admission_number'
    )
    
    class Meta:
        model= Payment
        fields=['user','admission_number', 'admin_fee', 'course_fee','library_fee', 'total', 'status']
        
        

   
class ReceiptSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(source = 'payment.transaction_id', read_only = True, allow_null=True)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
    
        def format_currency(value):
            if value is not None:
                if getattr(settings, 'USE_L1ON', False):
                    from django.utils.numberformat import format_number
                    return format_number(value, grouping= True)
                else:
                    return "{:,.2f}".format(value)
            return None
        
        representation['admin_fee'] = format_currency(instance.admin_fee)
        representation['course_fee'] = format_currency(instance.course_fee)
        representation['library_fee'] = format_currency(instance.library_fee)
        representation['total_amount'] = format_currency(instance.total_amount)
        
        return representation
    
    
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['receipt_number', 'issue_date', 'student_name', 'admission_number', 'admin_fee', 'course_fee', 'library_fee', 'total_amount', 'payment_status', 'transaction_id']
        
        


class IdentityCardSerializer(serializers.ModelSerializer):
    admission_number = serializers.CharField(write_only=True, required=False) 

    faculty = serializers.SlugRelatedField(
        queryset=Student.objects.all(),
        slug_field='faculty',
        required=False,  
        allow_null=True
    )

    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(),
        slug_field='name',
        required=False, 
        allow_null=True
    )
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        error_messages={
            'does_not_exist': 'The user with the provided ID does not exist. Please provide a valid user ID.',
            'incorrect_type': 'Incorrect type for user ID. Expected a number.'
        }
    )

    class Meta:
        model = IdentityCard
        fields = ['user', 'admission_number', 'department', 'faculty', 'picture']
        read_only_fields = ['picture']

    def validate(self, data):
        user = data.get('user')
        
        if user.user_type != 'Student':
            raise ValidationError({"user":"Identity cards can only be created for students."})

         
        if user.user_type == 'Student' and not data.get('admission_number'):
            raise ValidationError({'admission_number': 'Admission number is required for students.'})
        
           
        if user.user_type == 'Student' and not data.get('faculty'):
            raise ValidationError({'faculty': 'Faculty is required for students.'})

        if user.user_type == 'Student' and not data.get('department'):
            raise ValidationError({'department': 'Department is required for students.'})
            
        return data

        

    def create(self, validated_data):
        admission_number_str = validated_data.pop('admission_number', None)  # Use pop with default
        user = validated_data['user'] # get user
        if user.user_type == 'Student': # only students should have admission number
            try:
                student = Student.objects.get(admission_number=admission_number_str)
            except Student.DoesNotExist:
                raise serializers.ValidationError(
                    {'admission_number': 'Student with this admission number does not exist.'})
            validated_data['admission_number'] = student
        return IdentityCard.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.admission_number:
            data['admission_number'] = instance.admission_number.admission_number
        else:
            data['admission_number'] = None

        if instance.department:
            data['department'] = instance.department.name
        else:
            data['department'] = None

        if instance.faculty:
            data['faculty'] = instance.faculty.faculty
        else:
            data['faculty'] = None
        return data



class ResultSerializer(serializers.ModelSerializer):
    admission_number = serializers.CharField(write_only=True)  # Override default FK behavior
    
    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(),
        slug_field='code'  
    )
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        error_messages={
            'does_not_exist': 'The user with the provided ID does not exist. Please provide a valid user ID.',
            'incorrect_type': 'Incorrect type for user ID. Expected a number.'
        }
    )

    class Meta:
        model = Result
        fields = ['user', 'admission_number', 'course', 'grade', 'exam', 'score']

    def validate(self, data):
        user = data.get('user')
        if user and user.user_type != 'Student':
            raise serializers.ValidationError({"user": "Only students can be assigned results"})
        return data

    def validate_admission_number(self, value):
        try:
            student = Student.objects.get(admission_number=value)
            return student
        except Student.DoesNotExist:
            raise serializers.ValidationError(f"No student found with admission number '{value}'")

    def create(self, validated_data):
        student = validated_data.pop('admission_number')
        return Result.objects.create(admission_number=student, **validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance) # gets Result Model
        data['admission_number'] = instance.admission_number.admission_number  # access Student Model using foreignkey and gains access to all objects there
        data['course'] = instance.course.code if instance.course else None
        return data


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model= Announcement
        fields = '__all__'
        
    def create(self, validated_data):
        announcements = Announcement.objects.create(**validated_data)
        announcements.save()
        return announcements
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields='__all__'
        
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        post.save()
        return post
    
class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields='__all__'
        
    def create(self, validated_data):
        repost = Repost.objects.create(**validated_data)
        repost.save()
        
        return repost
    

class Commentserializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        comment.save()
        
        return comment
    
class LectureSerializer(serializers.ModelSerializer):
    
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        error_messages={
            'does_not_exist': 'Course ID does not exist',
            'required': 'Course ID is required.'
        }
    )
    
    lecturer = serializers.StringRelatedField(read_only=True)
    
    
    class Meta:
        model = Lecture
        fields = ["course","lecturer","duration","start_time","venue"]
        
    def create(self, validated_data):
        validated_data.pop('lecturer', None)
        validated_data['lecturer'] = self.context['request'].user
        
        # print("Validated data before creating Lecture:", validated_data)
        lecture = Lecture.objects.create(**validated_data)
        return lecture
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.course:
            representation['course'] = instance.course.course_name #acceses all course model and gets course_name
        return representation
    
    
class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question 
        fields = [
            'text', 'is_image', 'option_a', 'option_b', 'option_c', 'option_d',
            'correct_option', 'mark'
        ]
        
    def validate(self, data):
        if not data.get('text') and not data.get('is_image'):
            raise ValidationError('Question must have either text or image')
        
        if data.get('text') and not data.get('is_image') and not all([data.get('option_a'), data.get('option_b'), data.get('option_c'), data.get('option_d')]):
            raise ValidationError('All (A, B, C, D) are required for text-based question')
        
        correct_option = data.get('correct_option')
        if correct_option not in ['A','B', 'C', 'D']:
            raise ValidationError("correct option must be either of A, B, C, D")
        
        return data
    
    
class ExamSerializer(serializers.ModelSerializer):
    
    questions = QuestionSerializer(many=True, required=False)
    
    # gets ForeignKey and returns str, not ID
    course = serializers.StringRelatedField(read_only=True)
    department = serializers.StringRelatedField(read_only=True)
    academic_session = serializers.StringRelatedField(read_only=True)
    
    # used for inputs only
    course_input = serializers.PrimaryKeyRelatedField(
        queryset = Course.objects.all(), source = 'course', write_only = True,
        error_messages = {'does not exist':"Course with this ID does not exist.", 
                          "required":"Course ID is required"}
    )
    department_input = serializers.PrimaryKeyRelatedField(
        queryset = Department.objects.all(), source = 'department', write_only =True,
        error_messages = {'does not exist':"Department with this ID does not exist",
                          "required":"Department ID is required"
                          }
    )
    academic_session_input = serializers.PrimaryKeyRelatedField(
        queryset = AcademicSession.objects.all(), source = 'academic_session', write_only=True,
        error_messages = {'does not exist':"Academic Session with this ID does not exist",
                          "required":"Session ID is required"
                          }
    )
    
    class Meta:
        model = Exam
        fields = [
            'id', 'course', 'department', 'date', 'duration', 'total_marks', 'semester',
            'academic_session', 'questions', 'course_input', 'department_input', 'academic_session_input'
        ]
        read_only_fields = ['id', 'academic_session', 'department', 'course']
    
    def validate(self, data):
        if data.get('date') and data['date'] < timezone.now().date():
            raise ValidationError({"date":"Exam date cannot be in the past"})
        
        # calls line 388
        questions_data = data.get('questions')
        if questions_data:
            sum_of_question_marks = sum(q.get('mark', 0) for q in questions_data)
            if sum_of_question_marks != data.get('total_marks'):
                raise ValidationError({"total_marks":"Total marks must match the sum of marks from all questions"})
            
        return data
    
    def create(self, validated_data):
        # pop gets/removes questions from question model and assigns to questions_data
        questions_data = validated_data.pop('questions', [])
        
        with transaction.atomic():
            exam = Exam.objects.create(**validated_data)
            
            for question_data in questions_data:
                Question.objects.create(exam=exam, **question_data)
                
        return exam
    
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None) #line 389 
        
        # gets validated_data, accesses attr and values e.g {"total_marks"} and its value e.g 100
        # items() returns validated_data as list of tuple, [('total_marks', 100)] e.t.c
        # attr gets key and value gets value
        # saves time from writing instance.field_name = value
        for attr, value in validated_data.items():
            # gets attribute, 
            setattr(instance, attr, value)
        instance.save()
        
        if questions_data is None:
            instance.question_set.all().delete()
            for question_data in questions_data:
                Question.objects.create(exam=instance, **question_data)
        return instance
    
    # Ensure all IDs are returned as str
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['questions'] = QuestionSerializer(instance.question_set.all(), many=True).data
        if instance.course:
            representation['course'] = str(instance.course)
        if instance.department:
            representation['department'] = str(instance.department)
        if instance.academic_session:
            representation['academic_session'] = str(instance.academic_session)
            
         # removes the IDs    
        representation.pop('course_id', None)
        representation.pop('department_id', None)
        representation.pop('academic_session_id', None)
        
        return representation
        
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
     
    def create(self, validated_data, request):
        user = CustomUser.objects.create(
        email = validated_data['email'], username = validated_data['username'],user_type = validated_data['user_type'])
        
        user.set_password(validated_data['password'])
        user.save()
        return user   
    
    
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id','event_name', 'description', 'event_date', 'start_time', 'end_time', 'event_type']
        
    def create(self, validated_data):
        calendar = Calendar.objects.create(**validated_data)
        calendar.save()
        return calendar
    
    #def
    

