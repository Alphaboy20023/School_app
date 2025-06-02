from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db import transaction
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
        

faculty_choices =[
    ("Faculty of Science","Faculty of Science"),
    ("Faculty of Arts","Faculty of Arts"),
    ("Faculty of Engineering","Faculty of Engineering"),
    ("Faculty of Education","Faculty of Education"),
    ("Faculty of Clinical Sciences","Faculty of Clinical Science"),
    ("Faculty of Commerce and Business","Faculty of Commerce and Business"),
    ("Fcaulty of Allied Health Sciences","Fcaulty of Allied Health Sciences"),
    ("Faculty of Law","Faculty of Law"),
    ("Faculty of Management Sciences","Faculty of Management Sciences"),
    ("School of Transport","School of Transport"),
    ("Faculty of Social Sciences","Faculty of Social Sciences"),
    ("School of Post Graduate Studies","School of Post Graduate Studies"),
]


class Student(TimeStampField):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type':UserTypes.STUDENT})
    date_of_birth=models.DateField(blank=True, null=True)
    current_session = models.ForeignKey('school_app.AcademicSession', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('school_app.Department', on_delete=models.SET_NULL, null=True)
    admission_number=models.CharField(max_length=50, unique=True, blank=True, null=True)
    faculty = models.CharField(choices=faculty_choices, max_length=50, blank=True)
    picture = models.ImageField(upload_to='students/', blank=True, null=True)
    level = models.PositiveSmallIntegerField(choices=[(100, '100'), (200, '200'), (300, '300'), (400, '400')], default=100)
    
    
    
    def get_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
    
    
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
    picture = models.ImageField(upload_to='lecturers/')
    
    def __str__(self):
        return f'{self.user.get_full_name()} - ({self.staff_id})'
    

class AcademicSession(TimeStampField):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f'{self.name}'
