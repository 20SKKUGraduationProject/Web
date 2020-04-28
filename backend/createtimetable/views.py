from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, base64
from course.models import Course
from .models import TimeTable
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
        credit8=request.POST.get('credit8')
        credit=[int(credit0),int(credit1),int(credit2),int(credit3),int(credit4),int(credit5),int(credit6),int(credit7),int(credit8)]

        #priority 계산
        courses = Course.objects.filter(school="83")
        pq = PriorityQueue()
        for c in courses:
            mealtime=1
            timevalid=1

            classes = c.class_day.split(',')

            for cl in classes:
                d = cl.split('【')
                if d[0]!="미지정":
                    weekday = d[0][:1]
                    times = d[0][1:].split('-')
                    start_time = datetime.datetime.strptime(times[0], "%H:%M")
                    end_time=datetime.datetime.strptime(times[1], "%H:%M")

                    if ((start_time<=datetime.datetime.strptime("12:00", "%H:%M"))&(datetime.datetime.strptime("12:00", "%H:%M")<end_time))|((start_time<datetime.datetime.strptime("13:00", "%H:%M"))&(datetime.datetime.strptime("13:00", "%H:%M")<=end_time))|((start_time<=datetime.datetime.strptime("18:00", "%H:%M"))&(datetime.datetime.strptime("18:00", "%H:%M")<end_time))|((start_time<datetime.datetime.strptime("19:00", "%H:%M"))&(datetime.datetime.strptime("19:00", "%H:%M")<=end_time)):
                        mealtime=0

                    for nt in nontime:
                        nt_weekday = nt[:1]
                        nt_start_time = datetime.datetime.strptime(nt[1:], "%H:%M")
                        nt_end_time = nt_start_time + datetime.timedelta(hours=1)
                        if (weekday==nt_weekday)&(((start_time <=nt_start_time)&(nt_start_time<end_time))|((start_time<=nt_start_time)&(nt_end_time<=end_time))|((start_time<nt_end_time)&(nt_end_time<=end_time))):
                            timevalid=0 

            class_rating = (float)(c.class_rating)
            prof_rating = (float)(c.prof_rating)
            if class_rating==-1:
                class_rating=2.5
            if prof_rating==-1:
                prof_rating=2.5

            priority = ((((class_rating+prof_rating)/2)**int(course_priority))/((mealtime+1)**int(meal_priority)))*timevalid
            pq.put(Course_pr(priority, c))

        result=[] #결과값 저장
        while not pq.empty():
            temp = pq.get()
            classes = temp.course.class_day.split(',')
            days=[]
            for cl in classes:
                d = cl.split('【')
                if d[0]!="미지정":
                    weekday = d[0][:1]
                    times = d[0][1:].split('-')
                    start_time = datetime.datetime.strptime(times[0], "%H:%M")
                    end_time=datetime.datetime.strptime(times[1], "%H:%M")
                    days.append([weekday, start_time, end_time])
                
            exist=False
            for r in result:
                #이미 해당하는 과목 들어가있는지 확인
                if temp.course.courseName==r.courseName:
                    exist=True
                    break

                #겹치는 시간이 있는지 확인
                r_classes = r.class_day.split(',')
                r_days=[]
                for r_cl in r_classes:
                    d = r_cl.split('【')
                    if d[0]!="미지정":
                        r_weekday = d[0][:1]
                        r_times = d[0][1:].split('-')
                        r_start_time = datetime.datetime.strptime(times[0], "%H:%M")
                        r_end_time=datetime.datetime.strptime(times[1], "%H:%M")
                        r_days.append([r_weekday, r_start_time, r_end_time])

                for d in days:
                    for r_d in r_days:
                        if (d[0]==r_d[0])&(((d[1] <=r_d[1])&(r_d[1]<d[2]))|((d[1]<=r_d[1])&(r_d[2]<=d[2]))|((d[1]<r_d[2])&(r_d[2]<=d[2]))):
                            exist=True
                            break
                    if exist==True:
                        break

                if exist==True:
                    break

            
            if exist==False:
                #creditvalid확인
                cr = temp.course.credit_time.split('(')
                if temp.course.Credit2=="전공핵심":
                    if credit[0]-int(cr[0])>=0:
                        credit[0]-=int(cr[0])
                        result.append(temp.course)
                elif temp.course.Credit2=="전공일반":
                    if credit[1]-int(cr[0])>=0:
                        credit[1]-=int(cr[0])
                        result.append(temp.course)
                elif temp.course.Credit2=="실험실습":
                    if credit[2]-int(cr[0])>=0:
                        credit[2]-=int(cr[0])
                        result.append(temp.course)
                '''
                elif temp.course.Credit2=="인문/사회":
                elif temp.course.Credit2=="과학/기술":
                elif temp.course.Credit2=="글로벌":
                elif temp.course.Credit2=="인성":
                elif temp.course.Credit2=="리더십":
                elif temp.course.Credit2=="일반교양":
                '''
        
        all_courses=""
        for r in result:
            all_courses+=r.courseID+" "

        timetable = TimeTable(
            studentID=username,
            studentName=userNameKo,
            courses=all_courses,
        )
        print(timetable.courses)
        if all_courses=="":
            print("empty courses!")
        else:
            timetable.save()

        context = {'username': username, 'userNameKo': userNameKo}
        return render(request, '../templates/dashboard.html', context)


class Course_pr:
    def __init__(self, pr, course):
        self.pr = pr
        self.course = course

    def __lt__(self, other):
        return self.pr > other.pr