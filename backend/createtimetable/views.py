from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, base64
from course.models import Course
from queue import PriorityQueue
import datetime

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
            mealtime=1
            timevalid=1

            classes = c.class_day.split(',')
            days=[]
            for cl in classes:
                d = cl.split('【')
                if d[0]!="미지정":
                    weekday = d[0][:1]
                    times = d[0][1:].split('-')
                    start_time = datetime.datetime.strptime(times[0], "%H:%M")
                    end_time=datetime.datetime.strptime(times[1], "%H:%M")
                    days.append([weekday, start_time, end_time])

                    if ((start_time<=datetime.datetime.strptime("12:00", "%H:%M"))&(datetime.datetime.strptime("12:00", "%H:%M")<end_time))|((start_time<datetime.datetime.strptime("13:00", "%H:%M"))&(datetime.datetime.strptime("13:00", "%H:%M")<=end_time))|((start_time<=datetime.datetime.strptime("18:00", "%H:%M"))&(datetime.datetime.strptime("18:00", "%H:%M")<end_time))|((start_time<datetime.datetime.strptime("19:00", "%H:%M"))&(datetime.datetime.strptime("19:00", "%H:%M")<=end_time)):
                        mealtime=0

                    for nt in nontime:
                        nt_weekday = nt[:1]
                        nt_start_time = datetime.datetime.strptime(nt[1:], "%H:%M")
                        nt_end_time = nt_start_time + datetime.timedelta(hours=1)
                        if ((start_time <=nt_start_time)&(nt_start_time<end_time))|((start_time<nt_end_time)&(nt_end_time<=end_time)):
                            timevalid=0 

            print(days)
            print(mealtime)
            print(timevalid)
            class_rating = (float)(c.class_rating)
            prof_rating = (float)(c.prof_rating)
            if class_rating==-1:
                class_rating=2.5
            if prof_rating==-1:
                prof_rating=2.5

            priority = ((((class_rating+prof_rating)/2)**int(course_priority))/((mealtime+1)**int(meal_priority)))*timevalid
            print(priority)


        context = {'username': username, 'userNameKo': userNameKo}
        return render(request, '../templates/dashboard.html', context)
