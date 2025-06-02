from django.contrib import admin
from accounts_app.models import  LecturerProfile, Student, CustomUser
# Register your models here.


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department','admission_number','faculty','level')
    
    def age_display(self, obj):
        return obj.get_age()
    age_display.short_description = 'age'
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'id')
    
class LecturerAdmin(admin.ModelAdmin):
    list_display=('user', 'rank', 'office_location')
    
admin.site.register(LecturerProfile, LecturerAdmin)
admin.site.register(Student, StudentProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)