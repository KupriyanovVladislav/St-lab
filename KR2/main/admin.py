from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Student, Teacher, Mark


class StudentAdmin(ModelAdmin):
    list_display = ('name', 'surname', 'birthdate')


class TeacherAdmin(ModelAdmin):
    list_display = ('name', 'surname', 'birthdate')


class MarkAdmin(ModelAdmin):
    list_display = ('value', 'student', 'teacher', 'date')


admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Mark, MarkAdmin)
