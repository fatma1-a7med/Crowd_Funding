

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterationForm(UserCreationForm):
    mobile_phone = forms.RegexField(regex=r'^\+?20?1[0-9]{9}$')    
    profile_picture=forms.ImageField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password1','password2','mobile_phone','profile_picture')
    
 