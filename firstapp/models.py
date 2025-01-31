from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=200, default=1)
    status = models.IntegerField(default=0)

class Teacher(models.Model):
    course = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    Age = models.IntegerField()
    Phone_number = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='image/', null=True, blank=True)

class Student(models.Model):
    course = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    Age = models.IntegerField()
    Phone_number = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='simage/', null=True, blank=True)