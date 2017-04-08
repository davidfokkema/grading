import argparse
import os
import time

import django
from django.core.files.base import ContentFile

os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()

from grading import utils
from grading.models import Report, Assignment


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Process assessments at the specified URL.")
    parser.add_argument('assignment_id')
    parser.add_argument('url')
    args = parser.parse_args()

    added, updated, unknown = [], [], []
    url = args.url
    assignment = Assignment.objects.get(pk=args.assignment_id)
    sheets = utils.get_sheets_from_url(url)
    for sheet in sheets:
        name = sheet['properties']['title']
        try:
            student = utils.get_student_from_name(name)
        except utils.IdentificationError:
            unknown.append(name)
        else:
            while True:
                pdf = utils.get_pdf_from_sheet_url(url, sheet)
                if b'%PDF' in pdf[:4]:
                    break
                else:
                    print("Error retrieving PDF, retrying...")
                    time.sleep(5)
            try:
                report = Report.objects.get(assignment=assignment,
                                            student=student)
                updated.append(student)
            except Report.DoesNotExist:
                report = Report(assignment=assignment, student=student)
                added.append(student)
            filename = "Checklist %s %s.pdf" % (assignment.title, student)
            report.assessment.save(filename, ContentFile(pdf))
            mark = utils.get_mark_from_sheet_url(url, sheet, 'E17')
            print(student, mark)
            report.mark = mark
            report.save()

    print("Added students:", added)
    print("Updated students:", updated)
    print("Unknown students:", unknown)
