from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, base64
from createtimetable.models import TimeTable
from course.models import Course
from datetime import datetime, timedelta
from operator import itemgetter

# Create your views here.

def login(request):
    context=[]
    if(request.method)=='POST':
        username = request.POST.get('id')
        password = request.POST.get('pwd')
        check = userauth(username, password)
        if check['returnCode'] =='success':
            context = check
            logindata = {'username': username, 'password': password}
            context.update(logindata)
            request.session['userNameKo']=context['userNameKo']
            request.session['username']=context['username']
            return HttpResponseRedirect('dashboard/', context)#render(request, '../templates/dashboard.html', context)
        else:
            context = {'message' : "ID or Password does not match. Try again"}
            return HttpResponseRedirect('')#render(request, '../templates/login.html', context)
    else:
        username = request.session.get('username')
        userNameKo = request.session.get('userNameKo')
        context = {'userNameKo':userNameKo, 'username':username}
        if username!=None:
            return HttpResponseRedirect('dashboard/', context)
    return render(request, '../templates/login.html')


def userauth(id, pwd):
    password_bytes = pwd.encode('ascii')
    b64_password_bytes = base64.b64encode(password_bytes)
    b64_password = b64_password_bytes.decode('ascii')
    url = "https://login.skku.edu/loginAction"
    headers = {'Content-Type': 'application/json'}
    login_data = {'lang': 'ko', 'userid': id, 'userpwd': b64_password}
    r = requests.post(url, headers=headers, data = json.dumps(login_data))
    result = r.json()
    return result

def dashboard(request):
    username = request.session.get('username')
    userNameKo = request.session.get('userNameKo')
    print("dashboard activated!")
    week_courses = loadTimeTable(username)
    print(week_courses)
    if(week_courses != None):
        context = {'username': username, 'userNameKo': userNameKo, "timetable": week_courses}
    else:
        context = {'username': username, 'userNameKo': userNameKo}
    return render(request, '../templates/dashboard.html', context)

def loadTimeTable(username):
    timetable = TimeTable.objects.filter(studentID=username).last()
    if timetable == None:
        return None
    courses = timetable.courses.split(' ')
    
    week=[[],[],[],[],[]]
    for c in courses:
        course = Course.objects.filter(school='83', courseID=c)
        
        if course.count()!=0:
            course = course.first()
            print(course.courseID+" "+course.courseName)

            classes = course.class_day.split(',')
            for cl in classes:
                d = cl.split('【')
                if d[0]!="미지정":
                    weekday = d[0][:1]
                    times = d[0][1:].split('-')
                    
                    if weekday=="월":
                        week[0].append([times[0], times[1], course.courseID, course.courseName, course.profName])
                    elif weekday=="화":
                        week[1].append([times[0], times[1], course.courseID, course.courseName, course.profName])
                    elif weekday=="수":
                        week[2].append([times[0], times[1], course.courseID, course.courseName, course.profName])
                    elif weekday=="목":
                        week[3].append([times[0], times[1], course.courseID, course.courseName, course.profName])
                    elif weekday=="금":
                        week[4].append([times[0], times[1], course.courseID, course.courseName, course.profName])
            
    for w in week:
        w.sort(key=lambda date: datetime.strptime(date[0], "%H:%M"))
            
    for d in range(0,len(week)):
        for i in range(0,len(week[d])):
            w = week[d][i]
            start_time = datetime.strptime(w[0], "%H:%M")
            end_time=datetime.strptime(w[1], "%H:%M")
            minute = (end_time-start_time).seconds/60
            space=0
            if (i!=0):
                _w = week[d][i-1]
                _start_time = datetime.strptime(_w[0], "%H:%M")
                _end_time=datetime.strptime(_w[1], "%H:%M")
                space=(start_time-_end_time).seconds/60

            w.append(minute) #수업시간
            w.append(space) #앞수업과 시간간격
                 
    return week
