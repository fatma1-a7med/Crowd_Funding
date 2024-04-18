from django import forms

from django import forms

class ProjectSearchForm(forms.Form):
    query = forms.CharField(label="Search Projects", required=False)
