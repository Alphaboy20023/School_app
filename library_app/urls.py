from django.urls import path


from .views import  BookRecordView, PhysicalBookView, EbookView
from school_inventory import settings



urlpatterns = [
    path('api/token/lend_book/', BookRecordView.as_view(), name='borrow_book'),
    path('api/token/physical_books/', PhysicalBookView.as_view(), name='physical_books'),
    path('api/token/e_books/', EbookView.as_view(), name='e_books'),
] 