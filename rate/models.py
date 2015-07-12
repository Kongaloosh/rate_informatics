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
    month = models.IntegerField()
    day = models.IntegerField()
    lecturer = models.ManyToManyField(Lecturer)
    course = models.ManyToManyField(Course)

    @classmethod
    def create(cls, year, month, day, lecturer):
        if(isinstance(year, int) and isinstance(month, int) and isinstance(day, int)):
            return cls(year=year, month=month, day=day, lecturer=lecturer)