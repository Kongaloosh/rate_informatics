from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.context_processors import csrf #protects from people spoofing authentication requests
from forms import *
from models import *
import logging
from datetime import datetime


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
    c.update(csrf(request))

    if request.method == 'POST':
        form = CourseForm(request.POST)     # create a form instance from request
        title = request.POST.get('inputName')
        initials = request.POST.get('inputInitials')
        if title and initials:

            try:
                obj = Course.objects.get(title=title)
                c['message'] = 'A course with this title exists.'
                return render_to_response("rate/add_a_course.html", c)
            except:
                pass

            try:
                obj = Course.objects.get(initials=initials)
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
        return render_to_response("rate/add_a_course.html", c)


def lecturer(request, first_name, last_name):
    c = {'lecturer': Lecturer.objects.get(first_name=first_name.title(), last_name=last_name.title())}
    return render_to_response('rate/lecturer.html', c)


def lecturers(request):
    c = {'lecturers': Lecturer.objects.all()}
    return render_to_response('rate/lecturer_list.html', c)


def add_a_lecturer(request):
    c = {}
    c.update(csrf(request))
    logger.debug(request.POST)
    if request.method == 'POST':
        first_name = request.POST.get('inputName')
        last_name = request.POST.get('inputSurname')
        if first_name and last_name:
            try:
                obj = Lecturer.objects.get(first_name=first_name, last_name=last_name)
                c['message'] = 'A lecturer with this name already exists.'
                return render_to_response("rate/add_a_lecturer.html", c)
            except:
                lecturer_form = Lecturer.create(first_name=first_name, last_name=last_name)
                lecturer_form.save()
                return HttpResponseRedirect('/')
        else:
            c['message'] = 'your form was invalid'
            return render_to_response("rate/add_a_lecturer.html", c)
    elif request.method == 'GET':
        return render_to_response("rate/add_a_lecturer.html", c)


def response(request):
    pass


def add_a_response(request):
    c = {}
    c.update(csrf(request))
    c.update({'lecturers': Lecturer.objects.all()})
    c.update({'courses': Course.objects.all()})
    c['message'] = None
    if request.method == 'POST':
        course_initials = request.POST.get('course')
        lecturer_1 = request.POST.get('lecturer_1').split(' ')
        lecturer_2 = request.POST.get('lecturer_2').split(' ')
        year = int(request.POST.get('year'))
        semester = int(request.POST.get('semester'))
        resp = request.POST.get('response')

        if course_initials and lecturer_1 and lecturer_2 and year and semester and resp:
            if semester != 1 and semester != 2:
                c['message'] = 'That semester doesn\'t exist, nerd.'
            if year > datetime.year:
                c['message'] = 'That year hasn\'t happened yet, cheeky.'
            if year < 1988:
                c['message'] = 'The department didn\'t exist then, cheeky.'
            if len(resp) > 1000:
                c['message'] = 'Could you make your response shorter, please? (1000 char max)'

            if c['message']:
                    return render_to_response("rate/add_a_response.html", c)
            cs = None

            try:
                cs = Course.objects.get(initials=course_initials)
            except:
                c['message'] = 'The course doesn\'t exist.'
                return render_to_response("rate/add_a_response.html", c)

            try:
                l = Lecturer.objects.get(first_name=lecturer_1[0], last_name=lecturer_1[1])
                rating = Rating.create(year=year, semester=semester, lecturer=l, course=cs, text=resp)
                rating.save()
                if lecturer_2[0].lower() != 'none':
                    try:
                        l = Lecturer.objects.get(first_name=lecturer_2[0], last_name=lecturer_2[1])
                        rating = Rating.create(year=year, semester=semester, lecturer=l, course=cs, text=resp)
                        rating.save()
                        return HttpResponseRedirect('/')
                    except:
                        c['message'] = 'Your second lecturer doesn\'t exist.'
                        return render_to_response("rate/add_a_response.html", c)
            except:
                c['message'] = 'Your first lecturer doesn\'t exist.'
                return render_to_response("rate/add_a_response.html", c)
    elif request.method == 'GET':
        return render_to_response("rate/add_a_response.html", c)

