from django import forms


class UploadReportForm(forms.Form):
    reports = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))


class UploadReportAssessmentForm(forms.Form):
    url = forms.URLField()
