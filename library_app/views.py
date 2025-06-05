from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from library_app.serializer import BookRecordSerializer, PhysicalBookSerializer, EBookSerializer
from .models import BookRecord, PhysicalBook, EBook
from rest_framework import status

# Create your views here.

class PhysicalBookView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = PhysicalBookSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def get(self, request):
        physical_books= PhysicalBook.objects.filter(user=request.user)
        serializer= PhysicalBookSerializer(physical_books, many=True)
        return Response(serializer.data)
    
    
class EbookView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer= EBookSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        e_books= EBook.objects.filter(user=request.user)
        serializer= EBookSerializer(e_books, many=True)
        return Response(serializer.data)


class BookRecordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = BookRecordSerializer (data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        transactions = BookRecord.objects.filter(
            user=request.user)
        serilizer = BookRecordSerializer(transactions, many = True)
        return Response(serilizer.data)
    
    

    

