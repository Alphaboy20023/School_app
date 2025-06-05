from rest_framework import serializers
from .models import CustomUser
from library_app.models import BookRecord, PhysicalBook, EBook
from django.utils import timezone

class PhysicalBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PhysicalBook
        fields= ['title', 'type', 'edition', 'author', 'summary', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
        
class EBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= EBook
        fields = ['title', 'file_format', 'download_link', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
        
    

class BookRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRecord
        fields = '__all__'
        read_only_fields= ['user', 'borrow_date', 'returned_date']
        
    def create(self, validated_data):
        user =self.context['request'].user
        validated_data['user'] = user
        
        validated_data['borrow_date'] = timezone.now()
        return BookRecord.objects.create(**validated_data)