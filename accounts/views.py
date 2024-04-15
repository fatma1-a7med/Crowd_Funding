from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.forms import  RegisterationForm,ProfileUpdateForm,PasswordVerificationForm
from accounts.models import Profile

# Create your views here.

def profile_view(request):
    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    first_name = current_user.first_name 
    last_name = current_user.last_name
    email = current_user.email
    profile = current_user.profile
    phone = profile.mobile_phone
    profile_picture = profile.profile_picture
    birthdate = profile.birthdate
    facebook_profile = profile.facebook_profile
    country = profile.country
        
    context = {
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'profile_picture': profile_picture,
            'birthdate': birthdate,
            'facebook_profile': facebook_profile,
            'country': country,
        }
    }

    return render(request, 'accounts/profile.html', context)



def update_profile(request):
    current_user = request.user
    profile = current_user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account.profile'))
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'accounts/update_profile.html', context)



def delete_account(request):
    if request.method == 'POST':
        password_form = PasswordVerificationForm(request.POST)
        if password_form.is_valid():
            # Verify the user's password
            user = request.user
            password = password_form.cleaned_data.get('password')
            if user.check_password(password):
                user.delete()
                return redirect('login')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
    else:
        password_form = PasswordVerificationForm()
    return render(request, 'accounts/delete_account_confirm.html', {'password_form': password_form})


def create_user(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Create a profile for the user
            Profile.objects.create(
                user=user,
                mobile_phone=form.cleaned_data['mobile_phone'],
                profile_picture=form.cleaned_data['profile_picture']
            )
            login(request, user)  # Log in the user after registration
            return redirect(reverse("login"))  # Redirect to login page after successful registration
    else:
        form = RegisterationForm()

    return render(request, 'accounts/register.html', {'form': form})