from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.forms import  RegisterationForm,ProfileUpdateForm,PasswordVerificationForm
from accounts.models import Profile

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.tokens import account_activation_token
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model,login

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


def index(request):
    messages_to_display= messages.get_messages(request)
    return render(request, "index.html" , {"messages" : messages_to_display})

def create_user(request):
    form = RegisterationForm()  

    if request.method == 'POST':
        form = RegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            
            Profile.objects.create(
                user=user,
                mobile_phone=form.cleaned_data['mobile_phone'],
                profile_picture=form.cleaned_data['profile_picture']
            )

            current_site= get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string("registration/account_activation_email.html",{
                "user":user,
                "domain":current_site.domain,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get("email")
            email=EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "please check your email to complete the registration")


            # Redirect to the index page after successful registration
            return redirect("index")
    return render(request, 'registration/register.html', {'form': form}) 

def activate(request,uidb64, token):
    User= get_user_model()

    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active =True
        user.save()

        login(request, user)
        messages.success(request, "Your account has been successfully activated")
        return redirect(reverse("login"))
    else:
        messages.error(request, "Activation link is invalid or expired")
        return redirect(reverse("index"))
