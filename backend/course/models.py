from django.db import models

# Create your models here.
class School(models.Model):
    Hakbu = models.CharField(max_length=200)
    Hakgwa = models.CharField(max_length=200, unique=True)

class Course(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='Hakbu_School')
    Campus = models.CharField(max_length=20) #캠퍼스
    courseID = models.CharField(max_length=20) #학수번호
    courseName = models.CharField(max_length=200) #교과목명
    Credit1 = models.CharField(max_length=20) #영역구분1
    Credit2 = models.CharField(max_length=20) #영역구분2
    year = models.CharField(max_length=10) #학년
    class_day = models.CharField(max_length=200) #수업요시및강의실
    class_type = models.CharField(max_length=20) #수업형태
    profName = models.CharField(max_length=200) #담당교수
    credit_time = models.CharField(max_length=10) #학점(시수)
    etc = models.CharField(max_length=200, null=True) #비고
    prof_rating = models.DecimalField(decimal_places=2, max_digits=1000, null=True)
    class_rating = models.DecimalField(decimal_places=2, max_digits=1000, null=True)

    def __str__(self):
        return self.courseID

class Student(models.Model):
    StudentID = models.IntegerField()
    year = models.IntegerField(null=True)
    Hakbu = models.CharField(max_length=200)
    Hakgwa = models.CharField(max_length=200)
    WantCredit1 = models.IntegerField(default=0)
    WantCredit2 = models.IntegerField(default=0)

    def __str__(self):
        return self.StudentID