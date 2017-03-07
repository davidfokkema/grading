from django import forms


class UploadReportForm(forms.Form):
    title = forms.CharField(max_length=100)
    reports = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))
