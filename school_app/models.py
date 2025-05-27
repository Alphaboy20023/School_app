from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db import models, transaction
from django.utils import timezone
from datetime import  date, timedelta
import datetime
from django.db.models import F
from decimal import Decimal
import uuid

# Create your models here.
class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserTypes(models.TextChoices):
    STUDENT= 'Student', 'Student'
    LECTURER= 'Lecturer', 'Lecturer'

class CustomUser(AbstractUser):

    # username = None
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(choices=UserTypes.choices, blank=True, null=True, max_length=20, default=UserTypes.STUDENT)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    is_admin = models.BooleanField(default=False)
    is_hod= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

class TimeStampField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # wont create this class in db except i call it
    class Meta:
        abstract = True


class AdmissionNumberCounter(models.Model):
    year = models.IntegerField(unique=True)
    last_number = models.IntegerField(default=0)

    @classmethod
    def get_next_number(cls):
        year = datetime.datetime.now().year
        with transaction.atomic():
            counter, created = cls.objects.get_or_create(year=year, defaults={'last_number': 0})
            counter.last_number = F('last_number') + 1
            counter.save()
            return cls.objects.get(year=year).last_number

faculty_choices ={
    "Faculty of Science":"Faculty of Science",
    "Faculty of Arts":"Faculty of Arts",
    "Faculty of Engineering":"Faculty of Engineering",
    "Faculty of Education":"Faculty of Education",
    "Faculty of Clinical Sciences":"Faculty of Clinical Science",
    "Faculty of Commerce and Business":"Faculty of Commerce and Business",
    "Fcaulty of Allied Health Sciences":"Fcaulty of Allied Health Sciences",
    "Faculty of Law":"Faculty of Law",
    "Faculty of Management Sciences":"Faculty of Management Sciences",
    "School of Transport":"School of Transport",
    "Faculty of Social Sciences":"Faculty of Social Sciences",
    "School of Post Graduate Studies":"School of Post Graduate Studies",
    
}


class Student(TimeStampField):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type':UserTypes.STUDENT})
    date_of_birth=models.DateField(blank=True, null=True)
    current_session = models.DateField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)
    admission_number=models.CharField(max_length=50, unique=True, blank=True, null=True)
    faculty = models.CharField(choices=faculty_choices, max_length=50, blank=True)
    picture = models.ImageField(upload_to='media/', blank=True, null=True)
    
    
    

    def get_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
    
    
    def generate_admission_number(self):
        year = datetime.datetime.now().year
        next_number = AdmissionNumberCounter.get_next_number()
        return f'ADM{next_number:03d}'

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.admission_number:
            self.admission_number = self.generate_admission_number()
        
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"
    
    
class LecturerProfile(TimeStampField):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type':UserTypes.LECTURER})
    # department = 
    staff_id = models.CharField(max_length=100, null=True, blank=True)
    rank = models.CharField(max_length=100, blank=True, null=True) # maybe a professor, Doctor e.t.c
    office_location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='media/lecturers')
    
    def __str__(self):
        return f'{self.user.get_full_name()} - ({self.staff_id})'
    

class AcademicSession(TimeStampField):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f'{self.name}'
    
Status_choices= {
    'Paid':'Paid',
    'Pending':"Pending",
    'Not Paid':'Not Paid'
}

class Payment(TimeStampField):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    admission_number = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    admin_fee=models.DecimalField(max_digits=8, decimal_places=2)
    course_fee=models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    library_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00')) 
    total= models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    status=models.CharField(choices=Status_choices, blank=True, null=True, )
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.total = self.admin_fee + self.course_fee + self.library_fee
        super().save(*args, **kwargs)
        
        
        
class Receipt(TimeStampField):
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    student_name = models.CharField(max_length=250)
    admission_number = models.CharField(max_length=50)
    admin_fee = models.DecimalField(max_digits=8, decimal_places=2)
    course_fee = models.DecimalField(max_digits=8, decimal_places=2)
    library_fee = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    
    
    def generate_receipt_number(self): 
        now = timezone.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        unique_id = uuid.uuid4().hex[:8].upper()
        
        return f"RCPT-{year}{month}{day}-{unique_id}"
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
        super().save(*args, **kwargs)
            
            

semester_choices= {
    "First Semester":"First Semester",
    "Second Semester":"Second Semester"
}

class Course(TimeStampField):
    course_name = models.CharField(max_length=100)
    code= models.CharField(max_length=10, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    description= models.TextField(blank=True, null=True)
    credit_units= models.PositiveSmallIntegerField()
    level = models.PositiveSmallIntegerField()
    semester= models.CharField(max_length=20, choices=semester_choices)
    lecturer = models.ManyToManyField(CustomUser, related_name='teach_courses', limit_choices_to={'user_type':UserTypes.LECTURER})
    
    def __str__(self):
        return f'{self.code} - {self.course_name}'
    
    
class Lecture(TimeStampField):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration= models.DurationField(default=datetime.timedelta(hours=2, minutes=00))
    venue = models.CharField(max_length=150, blank=True)
    



class Department(TimeStampField):
    name= models.CharField(max_length=100, unique=True)
    dept_code = models.CharField(max_length=10, unique=True)
    faculty= models.CharField(max_length=100, choices=faculty_choices)
    hod= models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name="head_of_department")
    
    def __str__(self):
        return f'{self.name} - {self.dept_code}'
    


exam_choices = {
    'Test':'Test',
    'Main Exam':'Main Exam'
}

class Exam(TimeStampField):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    department= models.ForeignKey('Department', on_delete=models.CASCADE)
    date= models.DateField()
    duration= models.DurationField(default=datetime.timedelta(hours=2, minutes=30))
    total_marks= models.PositiveIntegerField()
    semester= models.CharField(max_length=100, choices=semester_choices)
    academic_session= models.ForeignKey('AcademicSession', on_delete=models.CASCADE, null=True)
    exam_type = models.CharField(choices=exam_choices, max_length=20, default='Main Exam')
    
    def __str__(self):
        return f'{self.semester} Exam - {self.academic_session}'
    
    
    
class Question(TimeStampField):
    exam= models.ForeignKey('Exam', on_delete=models.CASCADE)
    text = models.TextField()
    is_image= models.ImageField(upload_to='media/', blank=True, null=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B','B'
        ),('C', 'C'), ('D', 'D')])
    
    mark = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.text[:50]
    
    
class IdentityCard(TimeStampField):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    picture= models.ImageField(upload_to='media/')
    department= models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    admission_number = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='studentId', null=True)
    faculty = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='studentFaculty',null=True)
    
    def __str__(self):
        return f'ID Card - {self.user.username} - {self.admission_number}'


class Result(TimeStampField): 
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    admission_number= models.ForeignKey('Student', on_delete=models.CASCADE, null=True, related_name='studentResult')
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, null=True, blank=True)
    course= models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    score= models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade= models.CharField(max_length=2, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} - {self.course} - {self.grade} - {self.score} - {self.admission_number}'



class Announcement(TimeStampField):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    title= models.CharField(max_length=50, blank=True)
    information = models.CharField(max_length=10000, blank=True)



class Post(TimeStampField):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=5000, blank=True)
    content = models.CharField(max_length=5000, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts')
    
    
class Repost(Post, TimeStampField):
    original_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='original_repost'
    )
    reposted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    
class Comment(TimeStampField):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    description = models.TextField(max_length=150, blank=True)


class Notification(TimeStampField):
    user = models.ForeignKey(CustomUser,on_delete=models.Case)
    message= models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f'notification from {self.user.username} - {self.message[:50]}'


event_type_choices = {
    'Academic':'Academic',
    'Holiday':'Holiday',
    'Sport':'Sport',
    'Cultural':'Cultural',
    'Deadline':'Deadline'
}

class Calendar(TimeStampField):
    event_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=255, blank=True)
    event_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    event_type = models.CharField( choices=event_type_choices, default='Academic')
    
    class Meta:
        ordering = ['event_date', 'start_time']
        
    def __str__(self):
        return f'{self.event_name} on {self.event_date}'
    

day_choices = {
    'Monday':'Monday',
    'Tuesday':'Tuesday',
    'Wednesday':'Wednesday',
    'Thursday':'Thursday',
    'Friday':'Friday',
    'Saturday':'Saturday'
}

class TimeTable(TimeStampField):
    week_day = models.CharField( choices=day_choices, default='Monday')
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True)
    lecturer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'user_type': UserTypes.LECTURER}, null=True)
    academic_session = models.ForeignKey('AcademicSession', on_delete=models.CASCADE, null=True)
    semester = models.CharField(max_length=20, choices=semester_choices, null=True)
    duration= models.DurationField(default=datetime.timedelta(hours=2, minutes=00))
    venue = models.CharField(max_length=150, blank=True)
    
    
    #to sort each day by actual order, django sets alphabetically
    @property
    def day_of_week_order(self):
        days = {
            'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
            'Friday': 5, 'Saturday': 6, 'Sunday': 7
        }
        return days.get(self.day_of_week)
    
    def __str__(self):
        return f'{self.week_day} - {self.course} - {self.lecturer} - {self.venue}'



