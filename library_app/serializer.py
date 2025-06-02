from rest_framework import serializers
from .models import CustomUser
from library_app.models import BookRecord, PhysicalBook, EBook

class PhysicalBookserializer(serializers.ModelSerializer):
    author =_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = PhysicalBook
        fields= ['title', 'type', 'edition', 'author_name', 'summary', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
        
class EBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= EBook
        fields = ['title', 'file_format', 'download_link', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
    

class BookRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRecord
        fields = []