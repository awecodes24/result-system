from django.contrib import admin
from .models import Student, Subject, Result

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'full_name', 'semester', 'email']
    search_fields = ['roll_number', 'full_name']
    list_filter = ['semester']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'semester', 'credits']
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks', 'grade', 'exam_date']
    list_filter = ['grade', 'subject']
    search_fields = ['student__roll_number', 'student__full_name']