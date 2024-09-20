# streaming_api/views.py
 
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Streaming Server!")
