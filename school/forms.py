from django import forms
from django.contrib.auth.models import User
from . import models

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        
class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['roll_no','level','mobile','fee','status']

class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        
class TeacherForm(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields=['salary','mobile','status']

status_choices=(
    ('Present','Present'),
    ('Absent','Absent')
    )
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=status_choices, required=False)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()

class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
