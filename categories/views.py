from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponse
from categories.forms import CategoryModelForm
from categories.models import Category

# Create your views here.

def landing(request):
    return HttpResponse("<h1> Welcome to categories app </h1>")



def create_category(request):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    form = CategoryModelForm()
    if request.method =="POST":
        form = CategoryModelForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            print("New category created:",category)  # Add this line for debugging

            url = reverse("categories.index")
            return redirect(url)
    context = {
        'form': form,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }    

    return render(request,'categories/create.html',
                  context)


def categories_index(request):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    categories = Category.get_all_categories()
    context = {
        'categories':categories,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }
    return render(request,'categories/index.html',
                  context)


def category_show(request,id):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    category = get_object_or_404(Category, pk=id)
    context = {
        'category':category,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }
    return render(request,'categories/show.html',
                  context)


def category_edit(request, id):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    category = get_object_or_404(Category, pk=id)
    form = CategoryModelForm(instance=category)
    if request.method == "POST":
        form = CategoryModelForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories.index')
    context = {
        'form': form,
        'category': category,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }    
    return render(request, 'categories/edit.html', context)


def category_delete(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    # return HttpResponse("project deleted")
    return redirect(reverse("categories.index"))

# def show_category_details(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     return render(request, 'categories/category_details.html', {'category': category})
