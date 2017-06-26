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

    for report in assignment.report_set.filter(mail_is_sent=False):
        enrollment = Enrollment.objects.get(course=assignment.course, student=report.student)
        if enrollment.is_active:
            print("Sending mail to %s" % report.student)
            context = Context({'student': report.student})
            body = mail_template.render(context)
            email = EmailMessage(subject=subject, body=body,
                                 to=[report.student.email],
                                 bcc=['d.b.r.a.fokkema@uva.nl'])
            try:
                email.attach_file(report.report.path)
            except ValueError:
                print("Not including report for student %s" % report.student)
            email.attach_file(report.assessment.path)
            email.send()
            report.mail_is_sent = True
            report.save()
        else:
            print("Not sending mail to %s as student has dropped out" % report.student)
