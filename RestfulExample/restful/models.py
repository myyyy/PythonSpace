# coding=utf-8
from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=50)

