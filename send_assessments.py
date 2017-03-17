import argparse
import os

import django
from django.template import Template, Context
from django.core.mail import EmailMessage

os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()

from grading.models import Report, Assignment


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Send assessments using email for specified assignment.")
    parser.add_argument('assignment_id')
    args = parser.parse_args()

    assignment = Assignment.objects.get(pk=args.assignment_id)
    mail_template = Template(assignment.mail_body)
    subject = assignment.mail_subject

    for report in assignment.report_set.filter(mail_is_sent=False):
        print("Sending mail to %s" % report.student)
        context = Context({'student': report.student})
        body = mail_template.render(context)
        email = EmailMessage(subject=subject, body=body,
                             to=[report.student.email],
                             bcc=['d.b.r.a.fokkema@uva.nl'])
        email.attach_file(report.report.path)
        email.attach_file(report.assessment.path)
        email.send()
        report.mail_is_sent = True
        report.save()
