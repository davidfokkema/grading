from django.db import models

class Account(models.Model):

    ACCOUNT_CHOICES = [('bb_uva', 'Blackboard UvA'),
                       ('bb_vu', 'Blackboard VU')]

    user = models.CharField(max_length=20)
    unsafe_password = models.CharField(max_length=80)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES)

    def __str__(self):
        return '%s - %s' % (self.get_account_type_display(), self.user)


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
