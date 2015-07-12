from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.context_processors import csrf #protects from people spoofing authentication requests
from forms import *
from models import *

def index(request):
    return render(request, "rate/index.html")


def about(request):
    return render(request, "rate/about.html")


def course(request, course_initials):
    c = {'course': Course.objects.get(initials=course_initials)}
    return render_to_response('rate/course.html', c)


def courses(request):
    c = {'courses': Course.objects.all()}
    return render_to_response('rate/course_list.html', c)


def add_a_course(request):
    c = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CourseForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            course = Course.create(form.cleaned_data['inputInitials'], form.cleaned_data['inputName'])
            course.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    elif request.method == 'GET':
        c.update(csrf(request))
        print(c)
        return render_to_response("rate/add_a_course.html", c)




def add_a_lecturer(request):
    return render(request, "rate/add_a_lecturer.html")


def add_a_response(request):
    return render(request, "rate/add_a_response.html")

