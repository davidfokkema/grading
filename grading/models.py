from django.db import models


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('bb_uva', 'Blackboard UvA', 'http://blackboard.uva.nl'),
        ('bb_vu', 'Blackboard VU', 'http://bb.vu.nl/')]
    ACCOUNT_CHOICES = [(u[0], u[1]) for u in ACCOUNT_TYPES]
    URLS = {u[0]: u[2] for u in ACCOUNT_TYPES}

    user = models.CharField(max_length=20)
    unsafe_password = models.CharField(max_length=80)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES)

    @property
    def url(self):
        return self.URLS[self.account_type]

    def __str__(self):
        return '%s - %s' % (self.get_account_type_display(), self.user)


class Course(models.Model):
    title = models.CharField(max_length=80)
    course_id = models.CharField(max_length=20)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    prefix = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    student_id = models.IntegerField()
    course = models.ManyToManyField(Course)
