import argparse
import os

import django
from django.template import Template, Context
from django.core.mail import EmailMessage

os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()

from grading.models import Assignment, Enrollment


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Send assessments using email for specified assignment.")
    parser.add_argument('assignment_id')
    args = parser.parse_args()

    assignment = Assignment.objects.get(pk=args.assignment_id)
    mail_template = Template(assignment.mail_body)
    subject = assignment.mail_subject

    for skills in assignment.skills_set.filter(mail_is_sent=False):
        enrollment = Enrollment.objects.get(course=assignment.course,
                                            student=skills.student)
        if enrollment.is_active:
            print("Sending mail to %s" % skills.student)
            context = Context({'student': skills.student})
            body = mail_template.render(context)
            email = EmailMessage(subject=subject, body=body,
                                 to=[skills.student.email],
                                 bcc=['d.b.r.a.fokkema@uva.nl'])
            email.attach_file(skills.assessment.path)
            email.send()
            skills.mail_is_sent = True
            skills.save()
        else:
            print("Not sending mail to %s as student has dropped out" % skills.student)
