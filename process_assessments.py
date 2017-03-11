import argparse
import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()

from grading import utils
from grading.models import Report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Process assessments at the specified URL.")
    parser.add_argument('assignment_id')
    parser.add_argument('url')
    args = parser.parse_args()

    added, updated, unknown = [], [], []
    url = args.url
    assignment_id = args.assignment_id
    sheets = utils.get_sheets_from_url(url)
    for sheet in sheets:
        name = sheet['properties']['title']
        try:
            student = utils.get_student_from_name(name)
        except utils.IdentificationError:
            unknown.append(name)
        else:
            print(student)
            pdf = utils.get_pdf_from_sheet_url(
                url, sheet['properties']['sheetId'])
            try:
                report = Report.objects.get(assignment__pk=assignment_id,
                                            student=student)
                updated.append(student)
            except Report.DoesNotExist:
                report = Report(assignment=assignment, student=student)
                added.append(student)
            report.assessment = pdf
            report.save()
