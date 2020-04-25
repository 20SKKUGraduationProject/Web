from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, base64

# Create your views here.
def createtimetable(request):
    username = request.session.get('username')
    userNameKo = request.session.get('userNameKo')
    if username:
        context = {'username': username, 'userNameKo': userNameKo}
        return render(request, '../templates/createtimetable.html', context)

    return render(request, '../templates/createtimetable.html')
