from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'is_reported']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['user', 'comment', 'content']
        
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['img']


class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}), required=False)

    class Meta:
        model = Project
        fields = ['project_title', 'project_details', 'total_target',
                  'start_time', 'end_time', 'category', 'tags', 'img']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Title'})
        self.fields['project_details'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Description'})
        self.fields['tags'].widget.attrs.update({'class': 'form-check-input'})



        
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if not name:
          raise forms.ValidationError("Please enter a name.")
        if not description:
          raise forms.ValidationError("Please enter a description.")

        return cleaned_data
        