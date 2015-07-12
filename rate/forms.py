from django import forms

__author__ = 'alex'


class LecturerForm(forms.Form):
    first_name = forms.CharField(label='FirstName', max_length=100)
    Last_name = forms.CharField(label='FirstName', max_length=100)


class CourseForm(forms.Form):
    course_name = forms.CharField(label='Lecturer', max_length=100)
    course_initials = forms.CharField(label='FirstName', max_length=5)


class ResponseForm(forms.Form):
    lecturer_name = forms.CharField(label='Lecturer', max_length=100)
