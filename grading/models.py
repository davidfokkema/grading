from django.db import models


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('bb_uva', 'Blackboard UvA', 'https://blackboard.uva.nl'),
        ('bb_vu', 'Blackboard VU', 'https://bb.vu.nl/')]
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


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    prefix = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=40)
    student_id = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return ' '.join([self.first_name, self.prefix, self.last_name])


class Course(models.Model):
    title = models.CharField(max_length=80)
    course_id = models.CharField(max_length=20)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return '%s' % self.title


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    final_mark = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.student)


class Assignment(models.Model):
    ASSIGNMENT_CHOICES = [
        ('verslag', "Verslag"),
        ('expvaardigheden', "Experimentele vaardigheden"),
    ]

    title = models.CharField(max_length=80)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment_type = models.CharField(max_length=20,
                                       choices=ASSIGNMENT_CHOICES)
    mail_subject = models.CharField(max_length=100, blank=True, null=True)
    mail_body = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s (%s) - %s' % (self.title,
                                 self.get_assignment_type_display(),
                                 self.course)


class Report(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=3, decimal_places=1, blank=True,
                               null=True)
    report = models.FileField()
    assessment = models.FileField()
    mail_is_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return '%s - %s' % (self.assignment, self.student)


class Skills(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=3, decimal_places=1, blank=True,
                               null=True)
    assessment = models.FileField()
    mail_is_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return '%s - %s' % (self.assignment, self.student)
