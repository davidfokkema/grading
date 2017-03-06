from django import forms


class UploadReportForm(forms.Form):
    title = forms.CharField(max_length=100)
    report = forms.FileField()
