from django.urls import path
from . import views


urlpatterns =[
    path('create', views.createProject, name='createProject'),
    path('projectDetails/<int:id>', views.showProject, name="showProject"),
    path('home/', views.home, name="homePage"),
]