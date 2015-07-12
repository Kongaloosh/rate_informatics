from django import forms

__author__ = 'alex'


class LecturerForm(forms.Form):
    first_name = forms.CharField(label='FirstName', max_length=100)
    Last_name = forms.CharField(label='LastName', max_length=100)


class CourseForm(forms.Form):
    course_name = forms.CharField(label='inputName', max_length=100)
    course_initials = forms.CharField(label='inputInitials', max_length=5)


class ResponseForm(forms.Form):
    response = forms.CharField(label='Lecturer', max_length=100)
    semester = forms.IntegerField()
    year = forms.IntegerField()