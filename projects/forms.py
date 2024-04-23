from django import  forms
from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'project_details', 'total_target',
                  'start_time', 'end_time', 'category', 'tags']
        



class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['img']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'is_reported']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['user', 'comment', 'content']
        
        





# class ImageForm(forms.ModelForm):
#         class Meta:
#             model = Images
#             fields = ['img_url']

