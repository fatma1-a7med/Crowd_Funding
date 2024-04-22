from django.urls import path
from . import views
from projects.views import *
from projects.views import project_edit,project_delete,project_show




urlpatterns =[
    path('',views.perojects_index,name='projects.index'),
    path('add', views.add_project, name='createProject'),
    path('save' , views.save_project , name='saveProject'),
    path('<int:_id>', views.project_details , name="projectDetails"),
    path('comments/add', views.add_comment),
    path('donation/add', views.add_donation),
    path('rate', views.rate_project),
    path('project/report', views.report_project),
    path('comment/report', views.report_comment),
    path('comment/replay', views.add_reply),
    path('user/<int:user_id>/projects', views.user_projects, name='userProjects'),
    path('donations/<int:user_id>/', views.user_donations, name='user_donations'),
    path('some_error_page/', views.some_error_page, name='some_error_page'),
    path('project/delete/<int:id>', views.delete_project, name='delete_project'),
    path('<int:id>',project_show, name='project.show'),
    path('<int:id>/edit', project_edit, name='project.edit'),
    path('<int:id>/delete',project_delete,name='project.delete'),


    # path('index/', home, name="home"),


]

# delete_project