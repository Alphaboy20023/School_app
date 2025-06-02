from django.urls import path


from .views import  BookRecordView
from school_inventory import settings



urlpatterns = [
    path('api/token/lend_book/', BookRecordView.as_view(), name='borrow_book'), 
] 