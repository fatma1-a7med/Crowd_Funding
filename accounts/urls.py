from django.urls import path
from accounts.views import  profile_view, create_user,update_profile,delete_account, create_user,index,activate,logout_view
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('profile/', profile_view , name='account.profile'),
    path('profile/update/', update_profile, name='account.profile.update'),
    path('delete-account/', delete_account, name='account.delete'),
    path('register/',create_user, name='account.register' ),
    path('index/',index, name='index' ),
    path('activate/<str:uidb64>/<str:token>/',activate, name='activate' ),
    path('logged_out/',logout_view, name='logout' ),

    #########
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]