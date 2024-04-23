from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from accounts.models import *
from accounts.forms import *
from django.contrib.auth.decorators import user_passes_test, login_required

from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import *
from projects.forms import *
# from projects.forms import ProjectForm, ImageForm
# from projects.forms import CommentForm, ReplyForm
from categories.models import *
from categories.forms import *


def superuser_login(request):
    # if request.user.is_authenticated:
    #      return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('index.superuser')
        else:
            print ('login is required')
            pass

    return render(request, 'registeration/login.html')



def superuser_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='superuser_login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@superuser_required
def admin_view(request):
    return render(request, 'superuser/index.html')

@superuser_required
def user_list(request):
    profiles = Profile.objects.all()
    return render(request, 'crud/user/users.html', {'profiles': profiles})

@superuser_required
def user_delete(request, user_id):
    user = Profile.objects.get(user_id=user_id).user
    if user.is_superuser:
        messages.error(request, 'You cannot delete a superuser.')
    else:
        user.delete()
        messages.success(request, 'User deleted successfully.')
    return redirect('user_list')


### Project Views ###
@superuser_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'crud/projects/project_list.html', {'projects': projects})

@superuser_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'crud/projects/project_detail.html', {'project': project})

@superuser_required
def update_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'crud/projects/update_project.html', {'form': form})

@superuser_required
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'crud/projects/delete_project.html', {'project': project})

### Images Views ###

@superuser_required
def show_images(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    images = Images.objects.filter(project_id=project_id)
    return render(request, 'crud/projects/image_project.html', {'project': project, 'images': images})    

@superuser_required
def add_image(request, project_id):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.project_id = Project.objects.get(id=project_id)
            image.save()
            return redirect('show_image', project_id=project_id)
    else:
        form = ImageForm()
    return render(request, 'crud/projects/add_image.html', {'form': form})

@superuser_required
def delete_image(request, image_id, project_id):
    image = Images.objects.get(id=image_id)
    if request.method == 'POST':
        image.delete()
        return redirect('show_image', project_id=project_id)
    return render(request, 'crud/projects/delete_image.html', {'image': image})


### Comment Views ###

@superuser_required
def all_comments(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    comments = Comment.objects.filter(project_id=project_id)
    return render(request, 'crud/projects/allcomments.html', {'project': project, 'comments': comments})    

@superuser_required
def add_comment(request, project_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project_id = Project.objects.get(id=project_id)
            comment.save()
            return redirect('show_comments', project_id=project_id)
    else:
        form = CommentForm()
    return render(request, 'crud/projects/add_comment.html', {'form': form})


@superuser_required
def delete_comment(request, comment_id, project_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('show_comments', project_id=project_id)
    return render(request, 'crud/projects/delete_comment.html', {'comment': comment})

### Reply Views ###

@superuser_required
def all_replies(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    replies = Reply.objects.filter(comment__project_id=project_id)
    return render(request, 'crud/projects/allreplies.html', {'project': project, 'replies': replies})

@superuser_required
def add_reply(request):
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data['comment'].id
            comment = get_object_or_404(Comment, id=comment_id)
            user = request.user
            Reply(user=user, comment=comment, content=form.cleaned_data["content"]).save()
            # Redirect to the show_comments page for the relevant project
            return redirect('show_comments', project_id=comment.project_id.id)  
    else:
        form = ReplyForm()
    return render(request, 'crud/projects/add_reply.html', {'form': form})



@superuser_required
def delete_reply(request, reply_id, project_id):
    reply = Reply.objects.get(id=reply_id)
    if request.method == 'POST':
        reply.delete()
        return redirect('all_replies', project_id=project_id)
    return render(request, 'crud/projects/delete_reply.html', {'reply': reply})



###select featured project ##
@login_required
def toggle_featured(request, project_id):
    if request.method == "POST":
        selected_projects = request.POST.getlist('featured')
        project = get_object_or_404(Project, id=project_id)
        project.featured = not project.featured
        project.save()
        return redirect('index.superuser')
    else:
        return redirect('index.superuser')
    
    
  
  
  ## category ##  
def categories_index(request):
    categories = Category.get_all_categories()
    return render(request, 'crud/categories/index.html', {'categories': categories})


    
def category_create(request):
    if request.method == 'POST':
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_index')  # Change this to your desired URL after category creation
    else:
        form = CategoryModelForm()
    return render(request,'crud/categories/create.html',
                   {'form': form})



def category_show(request,id):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    category = get_object_or_404(Category, pk=id)
    context = {
        'category':category,
        # 'userData': {
        #     'user_id': user_id,
        #     'username': user_name,
        #     'profile_picture': profile_picture,
            
        # }
    }
    return render(request,'crud/categories/show.html',
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
            return redirect('categories_index')
    context = {
        'form': form,
        'category': category,
        # 'userData': {
        #     'user_id': user_id,
        #     'username': user_name,
        #     'profile_picture': profile_picture,
            
        # }
    }    
    return render(request, 'crud/categories/edit.html', context)


def category_delete(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    # return HttpResponse("project deleted")
    return redirect(reverse("categories_index"))
    