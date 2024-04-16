from django import  forms
from .models import Project, Images



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields=['title', 'details', 'totaltarget',
                  'start_date', 'end_date', 'category', 'tags']


class ImageForm(forms.ModelForm):
        class Meta:
            model = Images
            fields = ['img_url']
