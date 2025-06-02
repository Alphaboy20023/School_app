from django.contrib import admin
from .models import EBook, PhysicalBook, BookRecord
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author','quantity')
    search_fields = ('title', 'type')
    list_filter = ['type','author']
    
class EbookAdmin(admin.ModelAdmin):
    list_display = ('title','quantity','file_format')
    search_fields = ('title', )
    list_filter = ['title']
    
    
        

admin.site.register(PhysicalBook, BookAdmin)
admin.site.register(EBook, EbookAdmin)
admin.site.register(BookRecord)