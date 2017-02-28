from django.db import models

class Account(models.Model):
    user = models.CharField(max_length=20)
    unsafe_password = models.CharField(max_length=80)
    account_type = models.CharField(max_length=20,
                                    choices=[('blackboard', 'blackboard')])

class Course(models.Model):
    title = models.CharField(max_length=20)
    course_id = models.CharField(max_length=20)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class Student(models.Model):
    first_name = models.CharField(max_length=20)
    prefix = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    student_id = models.IntegerField()
    course = models.ManyToManyField(Course)
