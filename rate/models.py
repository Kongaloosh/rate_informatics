from django.db import models


class Lecturer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.DateTimeField('date published')


class Class(models.Model):
    initials = models.CharField()
    title = models.CharField()


class Rating(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    lecturers = models.ManyToManyField(Lecturer)