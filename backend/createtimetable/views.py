from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, base64

# Create your views here.
def createtimetable(request):
    return render(request, '../templates/createtimetable.html')
