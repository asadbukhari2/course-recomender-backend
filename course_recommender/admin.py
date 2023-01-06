from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *


# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'contact_no', 'state', 'zip_code', 'country']
    list_display_links = ['user']


class DegreeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['title']


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['title']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['name']


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'level']
    list_display_links = ['level']


class StudyModeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type']
    list_display_links = ['type']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'price', 'rating', 'credit_hours']
    list_display_links = ['name']


admin.site.register(Student, StudentAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Difficulty, DifficultyAdmin)
admin.site.register(StudyMode, StudyModeAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.unregister(Group)
