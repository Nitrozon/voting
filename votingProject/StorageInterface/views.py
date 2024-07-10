import csv
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import UploadCSVForm, StudentLoginForm
from .models import Candidate, Vote, Student



def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            admission_no = form.cleaned_data['admission_no']
            try:
                student = Student.objects.get(admission_no=admission_no)
                user = student  # Assuming Student is your user model
                login(request, user)
                return redirect('election:vote')  # Redirect upon successful login
            except Student.DoesNotExist:
                return render(request, 'election/login.html', {'error_message': 'Student not found.'})
        else:
            return render(request, 'election/login.html', {'form': form})
    else:
        form = StudentLoginForm()
        return render(request, 'election/login.html', {'form': form})
@login_required
def vote(request):
    if request.method == 'POST':
        if Vote.objects.filter(user=request.user).exists():
            print(f"User {request.user.username} has already voted.")
            return redirect('election:already_voted')

        candidate_id = request.POST.get('candidate')
        candidate = Candidate.objects.get(id=candidate_id)

        try:
            student = Student.objects.get(admission_no=request.user.username)
        except Student.DoesNotExist:
            print(f"Student record not found for user {request.user.username}")
            return redirect('election:already_voted')

        if student.is_teacher:
            votes_count = 2  # Double the vote count for teachers
        else:
            votes_count = 1

        for _ in range(votes_count):
            Vote.objects.create(user=request.user, candidate=candidate)
            candidate.votes += 1
            candidate.save()

        print(f"User {request.user.username} voted for {candidate.c_name}.")

        return redirect('election:results')

    candidates = Candidate.objects.all()
    return render(request, 'election/vote.html', {'candidates': candidates})

@login_required
def already_voted(request):
    return render(request, 'election/already_voted.html')  # Update template path

@login_required
def results(request):
    candidates = Candidate.objects.all()
    return render(request, 'election/results.html', {'candidates': candidates})  # Update template path

@login_required
def upload_csv(request):
    if request.method == 'POST':
        if 'upload_candidates_csv' in request.POST:
            csv_file = request.FILES['file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                Candi_no, c_name, department, year = row
                Candidate.objects.create(Candi_no=Candi_no, c_name=c_name, department=department, year=year)
            return redirect('election:results')

        elif 'upload_voters_csv' in request.POST:
            csv_file = request.FILES['file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                admission_no, name, student_class, has_voted = row
                try:
                    student = Student.objects.get(admission_no=admission_no)
                    student.name = name
                    student.student_class = student_class
                    student.has_voted = has_voted.lower() == 'true'
                    student.save()
                except Student.DoesNotExist:
                    Student.objects.create(admission_no=admission_no, name=name, student_class=student_class, has_voted=has_voted.lower() == 'true')

            return redirect('election:results')

        elif 'upload_teachers_csv' in request.POST:
            csv_file = request.FILES['file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                admission_no, name, student_class, has_voted = row
                try:
                    teacher = Student.objects.get(admission_no=admission_no)
                    teacher.name = name
                    teacher.student_class = student_class
                    teacher.has_voted = has_voted.lower() == 'true'
                    teacher.is_teacher = True
                    teacher.save()
                except Student.DoesNotExist:
                    Student.objects.create(admission_no=admission_no, name=name, student_class=student_class, has_voted=has_voted.lower() == 'true', is_teacher=True)

            return redirect('election:results')

        elif 'reset_all' in request.POST:
            Candidate.objects.all().delete()
            Vote.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            Student.objects.all().delete()

            return redirect('election:results')

    return render(request, 'election/upload_csv.html')

def voters_list(request):
    voters = Student.objects.all()
    return render(request, 'election/voters_list.html', {'voters': voters})
