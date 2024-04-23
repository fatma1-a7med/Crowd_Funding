from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile
from django.core.exceptions import ValidationError

from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


class RegisterationForm(UserCreationForm):
    mobile_phone = forms.RegexField(regex=r'^(\+?2?)?01[0-9]{9}$',
                                    error_messages={'invalid': 'Enter a valid Egyptian mobile phone number.'})

    profile_picture=forms.ImageField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name','password1','password2','username', 'email','mobile_phone','profile_picture')

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name.isalpha():
            raise ValidationError("First name should contain only alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name.isalpha():
            raise ValidationError("Last name should contain only alphabetic characters.")
        return last_name
    
    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists!!")
        return email
    

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30,required=True)
    email = forms.EmailField(disabled=True)
    mobile_phone = forms.RegexField(regex=r'^\+?20?1[0-9]{9}$',required=True)    
    birthdate = forms.DateField(required=False)
    facebook_profile = forms.URLField(required=False)
    country = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            user = instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError('Please enter a valid first name.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise ValidationError('Please enter a valid last name.')
        return last_name  

    def clean_country(self):
        country = self.cleaned_data['country']
        if not country.isalpha():
            raise ValidationError('Please enter a valid country name.')
        return country 

  
    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            profile.save()
            user.save()
        return profile


class PasswordVerificationForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    
 