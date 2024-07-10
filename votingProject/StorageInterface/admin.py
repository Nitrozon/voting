from django.contrib import admin
from .models import Student, Admin, Candidate, PseudoStudent

admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Candidate)
admin.site.register(PseudoStudent)
