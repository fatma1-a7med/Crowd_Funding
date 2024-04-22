from django import  forms
from .models import Project, Images



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields=['project_title', 'project_details', 'total_target',
                  'start_time', 'end_time', 'category','created_at', 'tags']


class ImageForm(forms.ModelForm):
        class Meta:
            model = Images
            fields = ['img']



# class ImageForm(forms.ModelForm):
#         class Meta:
#             model = Images
#             fields = ['img_url']

