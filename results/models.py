from django.db import models

# Create your models here.
class Student(models.Model):
    roll_number = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    semester = models.IntegerField(choices=[(i, f'Semester {i}') for i in range(1,9)])
    enrolled_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.roll_number} - {self.full_name}'
    
    class Meta:
        ordering = ['roll_number']
        

class Subject(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    semester = models.IntegerField()
    credits = models.IntegerField(default=3)
    
    def __str__(self):
        return f"{self.code}: {self.name}"
    
class Result(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),('A', 'A'), ('B+', 'B+'), ('B', 'B'),
        ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    full_marks  = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    exam_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject')
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade from marks percentage
        pct = (self.marks/ self.full_marks) * 100
        if pct >= 90: self.grade = 'A+'
        elif pct >= 80: self.grade = 'A'
        elif pct >= 70: self.grade = 'B+'
        elif pct >= 60: self.grade = 'B'
        elif pct >= 50: self.grade = 'C+'
        elif pct >= 45: self.grade = 'C'
        elif pct >= 35: self.grade = 'D'
        else:           self.grade = 'F'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code}: {self.grade}"