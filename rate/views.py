from django.shortcuts import render, HttpResponse


def index(request):
    return HttpResponse("Hey there, this is still in development. Hang tight")