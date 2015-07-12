from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, "rate/index.html")


def about(request):
    return render(request, "rate/about.html")


def add_a_course(request):
    return render(request, "rate/add_a_course.html")


def add_a_lecturer(request):
    return render(request, "rate/add_a_lecturer.html")


def add_a_response(request):
    return render(request, "rate/add_a_response.html")

