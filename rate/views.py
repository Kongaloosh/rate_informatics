from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, "rate/index.html")