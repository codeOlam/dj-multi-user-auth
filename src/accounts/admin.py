from django.contrib import admin

# Register your models here.
from .models import Users, Teacher, Student


admin.site.register(Users)
admin.site.register(Teacher)
admin.site.register(Student)