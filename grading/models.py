from django.db import models

class Account(models.Model):
    user = models.CharField()
    password = models.CharField()
    account_type = models.CharField(choices=[('blackboard', 'blackboard')])

class Course(models.Model):
    title = models.CharField()
    course_id = models.CharField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class Student(models.Model):
    first_name = models.CharField()
    prefix = models.CharField()
    last_name = models.CharField()
    course = models.ManyToManyField(Course)
