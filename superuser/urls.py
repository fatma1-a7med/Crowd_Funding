# urls.py
from django.urls import path,include
from superuser.views import *
from django.contrib import admin
from superuser.views import category_create,category_delete,category_show



urlpatterns = [
    path('log_in/', superuser_login, name='superuser_login'),
    path('index/', admin_view, name='index.superuser'),
    path('user_list/', user_list, name='user_list'),
    path('user_delete/<int:user_id>/', user_delete, name="user_delete"),

    ### Project URLs ###
    path('project/list/', project_list, name='project_list'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/update/', update_project, name='update_project'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),

    ### Images URLs ###
    path('project/<int:project_id>/image/show', show_images, name='show_image'),
    path('project/<int:project_id>/image/add/', add_image, name='add_image'),
    path('project/<int:image_id> <int:project_id>/image/delete/', delete_image, name='delete_image'),

    ### Comment URLs ###
    path('project/<int:project_id>/comment/show', all_comments, name='show_comments'),
    path('project/<int:project_id>/comment/add/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/<int:project_id>/', delete_comment, name='delete_comment'),



    ### Reply URLs ###
    path('project/<int:project_id>/reply/show/', all_replies, name='all_replies'),
    path('project/reply/add/', add_reply, name='add_reply'),
    path('reply/<int:reply_id>/delete/<int:project_id>/', delete_reply, name='delete_reply'),

### featured project##
   path('toggle_featured/<int:project_id>/', toggle_featured, name='toggle_featured'),
   
   
   
 ## category ##
 path('category/create/',category_create,name='category_create'),
 path('category/allcategory',categories_index,name='categories_index'),
 path('category/show/<int:id>', category_show, name='categories.show'),
 path('category/<int:id>/edit', category_edit, name='category_edit'),  
 path('category<int:id>/delete',category_delete,name='category_delete'),

]