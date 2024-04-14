from django.urls import path
from accounts.views import  profile_view, create_user,update_profile,delete_account
urlpatterns = [
    path('profile/', profile_view , name='account.profile'),
    path('profile/update/', update_profile, name='account.profile.update'),
    path('delete-account/', delete_account, name='account.delete'),
    path('register',create_user, name='account.register' )
]