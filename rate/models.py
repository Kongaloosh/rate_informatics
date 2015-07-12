from django.db import models


class Lecturer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    @classmethod
    def create(cls, first_name, last_name):
        return cls(first_name=first_name, last_name=last_name)


class Course(models.Model):
    initials = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    @classmethod
    def create(cls, initials, title):
        return cls(initials=initials.upper(), title=title)


class Rating(models.Model):
    year = models.IntegerField()
    semester = models.IntegerField()
    lecturer = models.ManyToManyField(Lecturer)
    course = models.ManyToManyField(Course)
    response = models.TextField(max_length=1000)

    @classmethod
    def create(cls, year, semester, lecturer, text):
        if(isinstance(year, int) and isinstance(semester, int)):
            return cls(year=year, semester=semester, lecturer=lecturer, reponse=text)