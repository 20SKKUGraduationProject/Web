from django.db import models

# Create your models here.
class TimeTable(models.Model):
    studentID = models.CharField(max_length=200)
    studentName = models.CharField(max_length=200)
    courses = models.CharField(max_length=200)

    def __str__(self):
        return self.studentID

