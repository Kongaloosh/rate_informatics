from django.db import models


class Lecturer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    @classmethod
    def create(cls, first_name, last_name):
        return cls(first_name=first_name, last_name=last_name)

    def __str__(self):
        return "{a} {b}".format(a=self.first_name, b=self.last_name)


class Course(models.Model):
    initials = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    @classmethod
    def create(cls, initials, title):
        return cls(initials=initials.upper(), title=title)

    def __str__(self):
        return "{a}".format(a=self.title)


class Rating(models.Model):
    year = models.IntegerField()
    semester = models.IntegerField()
    rating = models.TextField(max_length=1000)
    lecturer_1 = models.ForeignKey(Lecturer, related_name="first_lecturer")
    lecturer_2 = models.ForeignKey(Lecturer, null=True, default=None, related_name="second_lecturer")
    course = models.ForeignKey(Course)

    def __hash__(self):
        return hash(self.year)

    def __eq__(self, other):
        return self.course == other.course and \
               self.year == other.year and\
               self.semester == other.semester and\
               self.rating == other.rating

    @classmethod
    def create(cls, year, semester, lecturer_1, course, text, lecturer_2=None):
        if isinstance(year, int) and isinstance(semester, int):
            a = cls(year=year,
                    semester=semester,
                    course=course, rating=text,
                    lecturer_1=lecturer_1,
                    lecturer_2=lecturer_2)
            a.save()
            return a

    def __str__(self):
        return "{a}".format(a=self.rating[:20])