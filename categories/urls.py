from categories.views import landing
from django.urls import path
from categories.views import  *
# ,show_category_details

# include categories urls
urlpatterns = [
 path('categories',landing,name='categories'),
#  path('create',create_category,name='category'),
 path('',categories_index,name='categories.index'),
#  path('categories/<int:pk>/', show_category_details, name='categories.show'),
 path('<int:id>', category_show, name='categories.show'),
#  path('<int:id>/edit', category_edit, name='category.edit'),  # Add this line for category edit
#  path('<int:id>/delete',category_delete,name='category.delete'),

]
