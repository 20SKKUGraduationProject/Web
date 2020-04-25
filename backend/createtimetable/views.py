from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, base64
from course.models import Course
from queue import PriorityQueue

# Create your views here.
def createtimetable(request):
    username = request.session.get('username')
    userNameKo = request.session.get('userNameKo')
    if username:
        context = {'username': username, 'userNameKo': userNameKo}
        return render(request, '../templates/createtimetable.html', context)

    return render(request, '../templates/createtimetable.html')

def resulttimetable(request):
    if(request.method)=='POST':
        username = request.session.get('username')
        userNameKo = request.session.get('userNameKo')
        course_priority = request.POST.get('q1')
        meal_priority = request.POST.get('q2')
        nontime = request.POST.getlist('nontime')
        credit0=request.POST.get('credit0')
        credit1=request.POST.get('credit1')
        credit2=request.POST.get('credit2')
        credit3=request.POST.get('credit3')
        credit4=request.POST.get('credit4')
        credit5=request.POST.get('credit5')
        credit6=request.POST.get('credit6')
        credit7=request.POST.get('credit7')
        credit=[credit0,credit1,credit2,credit3,credit4,credit5,credit6,credit7]

        #priority 계산
        courses = Course.objects.filter(school="83")
        pq = PriorityQueue()
        for c in courses:
            print(c.class_day)

        context = {'username': username, 'userNameKo': userNameKo}
        return render(request, '../templates/dashboard.html', context)
