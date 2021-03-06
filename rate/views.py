from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.context_processors import csrf #protects from people spoofing authentication requests
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from forms import *
from models import *
import logging
from datetime import datetime
from itertools import chain

logger = logging.getLogger(__name__)


def index(request):
    c = {}
    c.update(csrf(request))
    c.update({'user': request.user})
    if request.method == 'POST':
        username = "user"
        password = request.POST.get('password').lower()
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                c['message'] = "You are now logged in. You can add information and browse the recommendations."
            else:
                c['message'] = "There's something wrong with your account."
        else:
            c['message'] = "The password is incorrect."
        return render_to_response('rate/index.html', c)
    else:
        return render_to_response("rate/index.html", c)


def about(request):
    return render(request, "rate/about.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def course(request, course_initials):
    try:
        c = {'course': Course.objects.get(initials=course_initials)}
        c['course_history'] = Rating.objects.filter(course=c['course']).distinct('year')
        review = []
        for i in c['course_history']:
            review.append(Rating.objects.filter(course=c['course'], year=i.year)).group
            c['reviews'] = review
    except:
        c = {'course': None}

    return render_to_response('rate/course.html', c)


@login_required(login_url='/')
def courses(request):
    c = {'courses': Course.objects.all().order_by('title')}
    return render_to_response('rate/course_list.html', c)


@login_required(login_url='/')
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
            return HttpResponseRedirect('/r/add')
        else:
            c.update(csrf(request))
            c['message'] = 'your form was invalid'
            return render_to_response("rate/add_a_course.html", c)
    # if a GET (or any other method) we'll create a blank form
    elif request.method == 'GET':
        return render_to_response("rate/add_a_course.html", c)


@login_required(login_url='/')
def lecturer(request, first_name, last_name):
    try:
        c = {'lecturer': Lecturer.objects.get(first_name=first_name.title(), last_name=last_name.title())}

    except:
        c = {'lecturer': None}
    try:
        a = Rating.objects.filter(lecturer_1=c['lecturer']).distinct('course')
    except:
        a = []
    try:
        b = c['taught_courses'] | Rating.objects.filter(lecturer_2=c['lecturer']).distinct('course')
    except:
        b = []

    c['taught_courses'] = set(list(chain(a, b)))

    review = []
    for i in c['taught_courses']:
        review.append(Rating.objects.filter(lecturer_1=i.lecturer_1, course=i.course))
        c['reviews'] = review

    return render_to_response('rate/lecturer.html', c)


@login_required(login_url='/')
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
                return HttpResponseRedirect('/r/add')
        else:
            c['message'] = 'your form was invalid'
            return render_to_response("rate/add_a_lecturer.html", c)
    elif request.method == 'GET':
        return render_to_response("rate/add_a_lecturer.html", c)


@login_required(login_url='/')
def lecturers(request):
    c = {'lecturers': Lecturer.objects.all().order_by('first_name')}
    return render_to_response('rate/lecturer_list.html', c)


def response(request):
    pass


@login_required(login_url='/')
def add_a_response(request):
    c = {}
    c.update(csrf(request))
    c.update({'lecturers': Lecturer.objects.all().order_by('first_name')})
    c.update({'courses': Course.objects.all().order_by('initials')})
    c['message'] = None

    if request.method == 'POST':
        course_initials = request.POST.get('course')
        lecturer_1 = request.POST.get('lecturer_1').split('_')
        lecturer_2 = request.POST.get('lecturer_2').split('_')

        if lecturer_1 == lecturer_2:
            lecturer_2 = None

        year = request.POST.get('year')
        semester = int(request.POST.get('semester'))
        resp = request.POST.get('response')

        if course_initials and lecturer_1 and lecturer_2 and year and semester and resp:
            year = int(year)
            if semester != 1 and semester != 2:
                c['message'] = 'That semester doesn\'t exist, nerd.'
            if year > datetime.now().year:
                c['message'] = 'That year hasn\'t happened yet, cheeky.'
            if year < 1988:
                c['message'] = 'The department didn\'t exist then, cheeky.'
            if len(resp) > 1000:
                c['message'] = 'Could you make your response shorter, please? (1000 char max)'

            if c['message']:
                return render_to_response("rate/add_a_response.html", c)
            try:
                cs = Course.objects.get(initials=course_initials)
            except:
                c['message'] = 'The course doesn\'t exist.'
                return render_to_response("rate/add_a_response.html", c)
            try:
                l = Lecturer.objects.get(first_name=lecturer_1[0], last_name=lecturer_1[1])
                if lecturer_2[0].lower() != 'none':
                    try:
                        l2 = Lecturer.objects.get(first_name=lecturer_2[0], last_name=lecturer_2[1])
                        rating = Rating.create(year=year, semester=semester, lecturer_1=l, lecturer_2=l2, course=cs, text=resp)
                        return HttpResponseRedirect('/course/{initials}'.format(initials = course_initials))
                    except:
                        c['message'] = 'Your second lecturer doesn\'t exist.'
                        return render_to_response("rate/add_a_response.html", c)
                else:
                    rating = Rating.create(year=year,
                                           semester=semester,
                                           lecturer_1=l,
                                           lecturer_2=None,
                                           course=cs,
                                           text=resp)
                    return HttpResponseRedirect('/course/{initials}'.format(initials = course_initials))
            except:
                c['message'] = 'Your first lecturer doesn\'t exist.'
                return render_to_response("rate/add_a_response.html", c)
        else:
            c['message'] = 'Your form isn\'t filled in properly.'
            return render_to_response("rate/add_a_response.html", c)
    elif request.method == 'GET':
        return render_to_response("rate/add_a_response.html", c)

