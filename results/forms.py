from django import forms
from .models import Student, Subject, Result

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'full_name', 'email', 'semester']
        widgets = {
            'roll_number': forms.TextInput(attrs={'placeholder': 'e.g. PUR080BCT001'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'student@ioe.edu.np'}),
            'semester': forms.Select()
        }
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'semester', 'credits']
        
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks', 'full_marks', 'exam_date']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'marks': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
        }
        
    def clean(self):
        cleaned = super().clean()
        marks = cleaned.get('marks')
        full_marks = cleaned.get('full_marks')
        if marks and full_marks and marks > full_marks:
            raise forms.ValidationError("Marks cannot exceed full marks.")
        return cleaned
    
class ResultSearchForm(forms.Form):
    roll_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Enter roll number...'}),
        label='Search by Roll Number'
    )