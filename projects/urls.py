from django.urls import path
from . import views


urlpatterns =[
    path('add', views.add_project, name='createProject'),
    path('save' , views.save_project , name='saveProject'),
    path('<int:_id>', views.project_details , name="projectDetails"),
    path('comments/add', views.add_comment),
    path('donation/add', views.add_donation),
    path('rate', views.rate_project),
    path('project/report', views.report_project),
    path('comment/report', views.report_comment),
    path('user/<int:user_id>/projects', views.user_projects, name='userProjects'),
    path('donations/<int:user_id>/', views.user_donations, name='user_donations'),
    path('some_error_page/', views.some_error_page, name='some_error_page')


]

