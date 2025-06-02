from django.contrib import admin
from school_app.models import (Payment, 
        Receipt, Department, Course, CustomUser, 
        Exam, Question, Result, IdentityCard, AcademicSession,
        Calendar, Post, TimeTable, Repost, Announcement, Comment, Lecture )


from datetime import date 

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display=('user','admission_number','admin_fee','course_fee','library_fee','total','status')

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('course_fee','library_fee','admin_fee','total_amount','receipt_number')
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'hod') 
       
    
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display= ('id', 'name', 'start_date', 'end_date')
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'text', 'correct_option', 'is_image')


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course)
admin.site.register(Exam)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(IdentityCard)
admin.site.register(Calendar)
admin.site.register(Post)
admin.site.register(TimeTable)
admin.site.register(Repost)
admin.site.register(Comment)
admin.site.register(Announcement)
admin.site.register(Lecture)


