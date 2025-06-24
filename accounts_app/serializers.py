from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from datetime import date
from django.conf import settings
from rest_framework.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from accounts_app.models import LecturerProfile, CustomUser, Student, UserTypes


class CustomUserTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user:
            data['customuser_Id'] = self.user.id
        return data 
    
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email','username','password','user_type', 'is_hod', 'is_staff', 'is_admin', 'is_superuser']
        extra_kwargs = {'password':{'write_only':True}}
        
        
    def create(self, validated_data):
        user = CustomUser.objects.create(
        email = validated_data['email'], username = validated_data['username'], user_type = validated_data['user_type'])
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, data):
        user_type= data.get('user_type')
        is_hod= data.get('is_hod', False)
        
        if is_hod and user_type != 'Lecturer':
            raise serializers.ValidationError({'is_hod':"only users with user_type= 'Teacher' can be HODs"})
        
        return data
    
    
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields= ['id','email','username','password', 'user_type']
        extra_kwargs= {
            'password':{'write_only': True}
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
        email = validated_data['email'], username = validated_data['username'],user_type = validated_data['user_type'])
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    


   
class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField(write_only=True)
    
    def validate(self, data):
        username= data.get('username')
        password= data.get('password')
        
        user= authenticate(username=username, password=password)
        
        if user is None:
           raise serializers.ValidationError('Invalid Username or Password')
        
        if not user.is_active:
            raise serializers.ValidationError('This account has been disabled')
        
        
        data['user']=user
        return data
        




class StudentSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    
    class Meta:
        model=Student
        fields= ['id', 'age', 'department','admission_number', 'Faculty','level']
        read_only_fields= ['age']
        
        
    
    def get_age(self, obj):
        if obj.date_of_birth:
            today = date.today()
            age = today.year - obj.date_of_birth.year
            if (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day):
                age -= 1
            return age
        return obj.get_age()

    def validate_date_of_birth(self, value):
        if relativedelta(date.today(), value).years < 17:
            raise serializers.ValidationError("Student must be at least 17 years old.")
        return value
        
    def validate_user(self,data):
        if data['user'] is None:
            raise serializers.ValidationError({'student does not exist'})
        return data
    
    
class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = ['id', 'user', 'department', 'rank']
        read_only = ['staff_id']
        
    def validate(self, data):
        if data['Lecturer'] is None:
            raise serializers.ValidationError({'Lecturer does not exist'})
        return data
    