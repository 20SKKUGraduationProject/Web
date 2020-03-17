from django.contrib import admin
from .models import School, Course, Student

# Register your models here.
admin.site.register(School)
admin.site.register(Course)
admin.site.register(Student)