from django.db import models
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
import datetime
from decimal import Decimal
import uuid
from accounts_app.models import TimeStampField, CustomUser, faculty_choices, UserTypes

# Create your models here.

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
    admission_number = models.ForeignKey('accounts_app.Student', on_delete=models.CASCADE, related_name='student')
    admin_fee=models.DecimalField(max_digits=8, decimal_places=2)
    course_fee=models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    library_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00')) 
    total= models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    status=models.CharField(choices=Status_choices, blank=True, null=True, )
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.admin_fee + self.course_fee + self.library_fee
        super().save(*args, **kwargs)
        
        
        
class Receipt(TimeStampField):
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    student_name = models.ForeignKey('accounts_app.Student', on_delete=models.SET_NULL, null=True)
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
            
            

semester_choices= [
    ("First Semester","First Semester"),
    ("Second Semester","Second Semester")
]

class Course(TimeStampField):
    course_name = models.CharField(max_length=100)
    code= models.CharField(max_length=10, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    description= models.TextField(blank=True, null=True)
    credit_units= models.PositiveSmallIntegerField()
    level = models.PositiveSmallIntegerField(choices=[(100, '100'), (200, '200'), (300, '300'), (400, '400')], default=100)
    semester= models.CharField(max_length=20, choices=semester_choices)
    lecturer = models.ManyToManyField(CustomUser, related_name='teach_courses', limit_choices_to={'user_type':UserTypes.LECTURER})
    
    def __str__(self):
        return f'{self.code} - {self.course_name}'
    
    
class Lecture(TimeStampField):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type':UserTypes.LECTURER})
    start_time = models.DateTimeField()
    duration= models.DurationField(default=datetime.timedelta(hours=2, minutes=00))
    venue = models.CharField(max_length=150, blank=True)
    



class Department(TimeStampField):
    name= models.CharField(max_length=100, unique=True)
    dept_code = models.CharField(max_length=10, unique=True)
    faculty= models.CharField(max_length=100, choices=faculty_choices)
    hod= models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name="head_of_department", limit_choices_to={'is_hod':True})
    
    def __str__(self):
        return f'{self.name} - {self.dept_code}'
    


exam_choices = [
    ('Test','Test'),
    ('Main Exam','Main Exam')
]

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
    is_image= models.ImageField(upload_to='exams/', blank=True, null=True)
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
    picture= models.ImageField(upload_to='students/')
    department= models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    admission_number = models.ForeignKey('accounts_app.Student', on_delete=models.CASCADE, related_name='studentId', null=True)
    faculty = models.CharField(choices=faculty_choices, max_length=50, default=None)
    
    def __str__(self):
        return f'ID Card - {self.user.username} - {self.admission_number}'


class Result(TimeStampField): 
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    admission_number= models.ForeignKey('accounts_app.Student', on_delete=models.CASCADE, null=True, related_name='studentResult')
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
    is_image = models.ImageField(upload_to='others/', null=True)
    
    
class Repost(Post):
    original_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='original_repost'
    )
    reposted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    
class Comment(TimeStampField):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    description = models.TextField(max_length=150, blank=True)


class Notification(TimeStampField):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,)
    message= models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f'notification from {self.user.username} - {self.message[:50]}'


event_type_choices = [
    ('Academic','Academic'),
    ('Holiday','Holiday'),
    ('Sport','Sport'),
    ('Cultural','Cultural'),
    ('Deadline','Deadline')
]


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
    

day_choices = [
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday')
]


class TimeTable(TimeStampField):
    week_day = models.CharField( choices=day_choices, default='Monday')
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True)
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': UserTypes.LECTURER}, null=True)
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
        return days.get(self.week_day)
    
    def __str__(self):
        return f'{self.week_day} - {self.course} - {self.lecturer} - {self.venue}'
