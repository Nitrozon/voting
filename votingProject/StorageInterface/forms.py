from django import forms
from .models import Student, Admin

class StudentLoginForm(forms.Form):
    admission_no = forms.CharField(label='Admission Number', max_length=100)

    def clean_admission_no(self):
        admission_no = self.cleaned_data['admission_no']
        try:
            student = Student.objects.get(admission_no=admission_no)
        except Student.DoesNotExist:
            raise forms.ValidationError("Student with this Admission Number does not exist.")
        return admission_no

class AdminLoginForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'password']

class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'password']

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()
