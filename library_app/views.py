from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from library_app.serializer import BookRecordSerializer
from .models import BookRecord

# Create your views here.

class PhysicalBookView(APIView):
    permission_classes=[IsAuthenticated]
    
    
    
class EbookView(APIView):
    permission_classes=[IsAuthenticated]


class BookRecordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = BookRecordSerializer (data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    def get(self, request):
        transaction = BookRecord.objects.filter(
            user=request.user)
        serilizer = BookRecordSerializer(transaction, many = True)
        return Response(serilizer.data)
    

