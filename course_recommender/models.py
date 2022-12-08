from django.db import models
from .enums import *

# Create your models here.


from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact_no = models.CharField(max_length=50)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city_name = models.TextField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    # avatar = models.FileField(upload_to=upload_profile_avatar, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class Degree(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.title


class Semester(models.Model):
    title = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class Difficulty(models.Model):
    level = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.level


class StudyMode(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.type


class Course(models.Model):
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    study_mode = models.ForeignKey(StudyMode, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    rating = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    credit_hours = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='cars')

    def __str__(self):
        # pass
        return self.name + " " + str(self.credit_hours) + " " + str(self.rating) + " " + str(self.price)
