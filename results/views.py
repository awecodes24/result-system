from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Student, Subject, Result
from .forms import StudentForm, SubjectForm, ResultForm, ResultSearchForm
from decimal import Decimal
import csv
from django.http import HttpResponse

GRADE_POINTS = {
    'A+': Decimal('4.0'), 'A': Decimal('3.75'),
    'B+': Decimal('3.5'), 'B': Decimal('3.0'),
    'C+': Decimal('2.5'), 'C': Decimal('2.0'),
    'D': Decimal('1.0'), 'F': Decimal('0.0'),
}

def calculate_gpa(results):
    """Calculate GPA weighted by subject credits."""
    if not results:
        return Decimal('0.0')
    total_points = sum(GRADE_POINTS[r.grade] * r.subject.credits for r in results)
    total_credits = sum(r.subject.credits for r in results)
    return round(total_points / total_credits, 2) if total_credits else Decimal('0.0')

@login_required
def dashboard(request):
    # Build grade distribution data for chart
    grade_counts = Result.objects.values('grade').annotate(count=Count('grade')).order_by('grade')
    grade_data = {item['grade']: item['count'] for item in grade_counts}

    context = {
        'total_students': Student.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_results': Result.objects.count(),
        'pass_count': Result.objects.exclude(grade='F').count(),
        'fail_count': Result.objects.filter(grade='F').count(),
        'avg_marks': Result.objects.aggregate(avg=Avg('marks'))['avg'] or 0,
        'recent_results': Result.objects.select_related('student', 'subject').order_by('-created_at')[:10],
        'grade_data': grade_data,
    }
    return render(request, 'results/dashboard.html', context)

@login_required
def student_list(request):
    query = request.GET.get('q', '')
    semester = request.GET.get('semester', '')
    students = Student.objects.all()
    if query:
        students = students.filter(full_name__icontains=query) | \
            students.filter(roll_number__icontains=query)
    if semester:
        students = students.filter(semester=semester)
    semesters = range(1, 9)
    return render(request, 'results/student_list.html',
                  {'students': students, 'query': query, 'semester': semester, 'semesters': semesters})

@login_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect('student_list')
    return render(request, 'results/add_student.html', {'form': form, 'title': 'Add Student'})

@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Student updated.")
        return redirect('student_list')
    return render(request, 'results/add_student.html', {'form': form, 'title': 'Edit Student'})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f"Student {student.full_name} deleted.")
        return redirect('student_list')
    return render(request, 'results/confirm_delete.html', {'object': student, 'object_type': 'Student'})

@login_required
def add_result(request):
    form = ResultForm(request.POST or None)
    if form.is_valid():
        result = form.save()
        messages.success(request, "Result saved successfully.")
        return redirect('student_report', pk=result.student.pk)
    return render(request, 'results/add_result.html', {'form': form})

@login_required
def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    results = Result.objects.filter(student=student).select_related('subject')
    gpa = calculate_gpa(list(results))
    passed = results.exclude(grade='F').count()
    failed = results.filter(grade='F').count()
    total_marks = sum(r.marks for r in results)
    total_possible = sum(r.full_marks for r in results)
    percentage = round((total_marks / total_possible) * 100, 2) if total_possible else 0
    return render(request, 'results/report.html', {
        'student': student,
        'results': results,
        'gpa': gpa,
        'passed': passed,
        'failed': failed,
        'percentage': percentage,
    })

@login_required
def search_result(request):
    form = ResultSearchForm(request.GET or None)
    student = None
    results = None
    gpa = None
    if form.is_valid():
        roll = form.cleaned_data['roll_number']
        try:
            student = Student.objects.get(roll_number=roll)
            results = Result.objects.filter(student=student).select_related('subject')
            gpa = calculate_gpa(list(results))
        except Student.DoesNotExist:
            messages.error(request, f"No student found with roll number '{roll}'.")
    return render(request, 'results/search.html', {'form': form, 'student': student, 'results': results, 'gpa': gpa})

@login_required
def export_csv(request, pk):
    student = get_object_or_404(Student, pk=pk)
    results = Result.objects.filter(student=student).select_related('subject')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{student.roll_number}_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['Subject Code', 'Subject Name', 'Credits', 'Marks', 'Full Marks', 'Grade'])
    for r in results:
        writer.writerow([r.subject.code, r.subject.name, r.subject.credits,
                         r.marks, r.full_marks, r.grade])
    return response
