from categories.views import landing
from django.urls import path
from categories.views import create_category, categories_index,category_show,category_edit,category_delete
# ,show_category_details

# include categories urls
urlpatterns = [
 path('categories',landing,name='categories'),
#  path('create',create_category,name='category'),
 path('',categories_index,name='categories.index'),
#  path('categories/<int:pk>/', show_category_details, name='categories.show'),
 path('<int:id>', category_show, name='categories.show'),
# path('category/show/<int:id>',category_show, name='category_show'),
#  path('<int:id>/edit', category_edit, name='category.edit'),
path('category/<int:id>/edit', category_edit, name='category_edit'),  

#  path('<int:id>/delete',category_delete,name='category.delete'),
  path('category<int:id>/delete',category_delete,name='category_delete'),


]
