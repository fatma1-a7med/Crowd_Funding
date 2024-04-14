from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from accounts.forms import  RegisterationForm
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
        
    context = {
        'userData': {
            'user_id':user_id,
            'username': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'profile_picture': profile_picture,
        }
    }

    return render(request, 'accounts/profile.html', context)


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