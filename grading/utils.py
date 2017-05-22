import re
from urllib.parse import urlencode

from .models import Student
from . import google_sheets, google_drive


class IdentificationError(Exception):
    pass


def get_student_from_filename(filename):
    """Try to guess and return the Student from a filename."""

    # treat space and underscore equally, as underscore
    filename = filename.replace(' ', '_')
    # try to get student id, at least 6 digits
    match = re.search('([0-9]{6,})', filename)
    try:
        # maybe there is no match, maybe there is not student
        student_id = match.group(1)
        return Student.objects.get(student_id=student_id)
    except (AttributeError, Student.DoesNotExist):
        pass
    # try to get student name, at least 5 characters, ignore leading
    # and trailing underscore
    match = re.search('([a-zA-Z_ ]{5,})', filename)
    name = match.group(1).strip('_')
    name = name.replace(' ', '_')
    name_parts = name.split('_')
    try:
        return Student.objects.get(first_name__icontains=name_parts[0],
                                   last_name__icontains=name_parts[-1])
    except Student.DoesNotExist:
        pass

    raise IdentificationError("Cannot find student.")


def get_student_from_name(name):
    name_parts = name.split(' ')
    try:
        return Student.objects.get(first_name__icontains=name_parts[0],
                                   last_name__icontains=name_parts[-1])
    except Student.DoesNotExist:
        raise IdentificationError("Cannot find student.")


def get_sheets_from_url(url):
    service = google_sheets.get_sheets_service()
    sheet_id = get_sheet_id_from_url(url)
    sheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    return sheet['sheets']


def get_sheet_id_from_url(url):
    pattern = 'https://docs.google.com/spreadsheets/d/([0-9a-zA-Z_-]+)/'
    match = re.match(pattern, url)
    return match.group(1)


def get_pdf_from_sheet_url(url, sheet, portrait=False):
    gid = sheet['properties']['sheetId']
    # strip off everything after the last slash
    url = re.match('.*/', url).group(0)
    params = urlencode({'format': 'pdf', 'portrait': portrait, 'gid': gid})
    export_url = url + 'export?' + params
    http = google_drive.get_authorized_http()
    response, content = http.request(export_url)
    return content


def get_value_from_sheet_url(url, sheet, cell):
    sheet_id = get_sheet_id_from_url(url)
    name = sheet['properties']['title']
    service = google_sheets.get_sheets_service()
    value = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=name + '!' + cell).execute()
    return value['values'][0][0]


def get_mark_from_sheet_url(url, sheet, cell):
    value = get_value_from_sheet_url(url, sheet, cell)
    mark = float(value.replace(',', '.'))
    return mark
