# coding: utf-8
import google_sheets
import google_drive
sheet_service = google_sheets.get_sheets_service()
sheet_id = "1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4"
sheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
sheet = sheet_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
sheet['sheets']
sheet['sheets'][0]
sheet['sheets'][0]['properties']
drive_service = google_drive.get_drive_service()
drive_service.files().export().get(fileId=sheet_id).execute()
drive_service.files().export(fileId=sheet_id)
drive_service.files().export(fileId=sheet_id, mimeType='application/pdf')
drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute()
sheet_id
drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute()
drive_service = google_drive.get_drive_service()
drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute()
with open('/Users/david/Desktop/test.pdf') as f:
    drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute()
    
with open('/Users/david/Desktop/test.pdf', 'w') as f:
    drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute()
    
with open('/Users/david/Desktop/test.pdf', 'w') as f:
    f.write(drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute())
    
    
data = drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute()
type(data)
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute())
    
    
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(drive_service.files().export(fileId=sheet_id, mimeType='application/pdf', gid='3452435').execute())
    
drive_service.files().export(gid=434)
help(drive_service.files().export)
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(drive_service.files().export(fileId=sheet_id, mimeType='application/pdf').execute())
    
    
credentials = google_drive.get_credentials()
http = credentials.authorize(httplib2.Http())
import httplib2
http = credentials.authorize(httplib2.Http())
http
help(http)
http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf')
v = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(v)
    
len(v)
v[0]
help(http.request)
help(http)
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf&portrait=false')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf&portrait=false')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf&portrait=false&pagenumbers=true')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf&portrait=false&pagenumbers=true&gid=')
response
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
sheet
sheet['sheets'][0]['properties']
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?mimeType=application/pdf&portrait=false&pagenumbers=true&gid=768596325')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?gid=768596325')
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?gid=768596325')
response
content
response, content = http.request('https://www.googleapis.com/drive/v3/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?gid=768596325&mimeType=application/pdf')
response
response, content = http.request('https://www.googleapis.com/drive/v2/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?gid=768596325&mimeType=application/pdf')
response
response, content = http.request('https://www.googleapis.com/drive/v1/files/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?gid=768596325&mimeType=application/pdf')
response
content
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export")
response
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?format=pdf")
response
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?format=pdf&portrait=false")
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?format=pdf&landscape=true")
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?format=pdf&portrait=false")
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?format=pdf&portrait=false&gid=768596325")
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
sheet['sheets'][3]['properties']
response, content = http.request("https://docs.google.com/spreadsheets/d/1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4/export?format=pdf&portrait=false&gid=2085546620")
with open('/Users/david/Desktop/test.pdf', 'wb') as f:
    f.write(content)
    
sheet = sheet_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
sheet['sheets'][3]['properties']
sheet_service().spreadsheets().values()
sheet_service.spreadsheets().values()
sheet_service.spreadsheets().values().get(spreadsheetId=1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4, range="Hapé Fuhri Snethlage!E17").execute()
sheet_service.spreadsheets().values().get(spreadsheetId="1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4", range="Hapé Fuhri Snethlage!E17").execute()
sheet_service.spreadsheets().values().get(spreadsheetId="1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4", range="Hapé Fuhri Snethlage!E17").execute()
sheet_service.spreadsheets().values().get(spreadsheetId="1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4", range="Hapé Fuhri Snethlage!E17").execute()
sheet_service.spreadsheets().values().get(spreadsheetId="1sFG2VwsEko1g6wVRmBoSuxj7hlpU8iEZt1_RE1QT5-4", range="Hapé Fuhri Snethlage!E17").execute()
get_ipython().magic('history')
get_ipython().magic('save playground.py')
