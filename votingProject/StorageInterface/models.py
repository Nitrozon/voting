from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    admission_no = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=100)
    has_voted = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)  # New field for teachers

    def __str__(self):
        return self.name


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Candidate(models.Model):
    Candi_no = models.IntegerField()
    c_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    votes = models.IntegerField(default=0)


class PseudoStudent(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    vot = models.IntegerField()


class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"