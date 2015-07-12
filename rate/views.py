from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.context_processors import csrf #protects from people spoofing authentication requests
from forms import *
from models import *
import logging


logger = logging.getLogger(__name__)


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
        form = CourseForm(request.POST)     # create a form instance from request
        title = request.POST.get('inputName')
        initials = request.POST.get('inputInitials')
        if title and initials:

            try:
                obj = Course.objects.get(title=title)
                c.update(csrf(request))
                c['message'] = 'A course with this title exists.'
                return render_to_response("rate/add_a_course.html", c)
            except:
                pass

            try:
                obj = Course.objects.get(initials=initials)
                c.update(csrf(request))
                c['message'] = 'A course with these initials exists.'
                return render_to_response("rate/add_a_course.html", c)
            except:
                pass

            course_form = Course.create(title=title, initials=initials)
            course_form.save()
            logger.debug(course_form.initials)
            return HttpResponseRedirect('/')
        else:
            c.update(csrf(request))
            c['message'] = 'your form was invalid'
            return render_to_response("rate/add_a_course.html", c)
    # if a GET (or any other method) we'll create a blank form
    elif request.method == 'GET':
        c.update(csrf(request))
        return render_to_response("rate/add_a_course.html", c)


def lecturer(request, first_name, last_name):
    c = {'lecturer': Lecturer.objects.get(first_name=first_name.title(), last_name=last_name.title())}
    return render_to_response('rate/lecturer.html', c)


def lecturers(request):
    c = {'lecturers': Lecturer.objects.all()}
    return render_to_response('rate/lecturer_list.html', c)


def add_a_lecturer(request):
    return render(request, "rate/add_a_lecturer.html")


def response(request):
    pass


def add_a_response(request):
    c = {}
    c.update({'lecturers': Lecturer.objects.all()})
    c.update({'courses': Course.objects.all()})
    return render_to_response("rate/add_a_response.html", c)

