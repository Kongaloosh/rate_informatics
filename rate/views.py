from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, "rate/index.html")


def about(request):
    return render(request, "rate/about.html")


def add_a_course(request):
    return render(request, "rate/add_a_course.html")