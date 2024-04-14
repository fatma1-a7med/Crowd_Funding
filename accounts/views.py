from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from accounts.forms import  RegisterationForm
# Create your views here.


def profile_view(request):
    url= reverse("homePage")
    return redirect(url)


def create_user(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect(reverse("login"))  # Redirect to login page after successful registration
    else:
        form = RegisterationForm()

    return render(request, 'accounts/register.html', {'form': form})