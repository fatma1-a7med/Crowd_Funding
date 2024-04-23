from django.db import models
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse,HttpResponseForbidden
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg, Sum,F
from django.contrib.auth.decorators import login_required
from .models import *
from projects.forms import ProjectForm





@login_required
def perojects_index(request):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    projects = Project.get_all_projects()
    context = {
        'projects':projects,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }
    return render(request,'user_projects/allprojects.html',
                  context)

@login_required
def add_project(request):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture  
    categories = Category.objects.all()       
    # if 'id' in request.session:
    context = {
        'categories': categories,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }
    return render(request, "user_projects/add_project.html",context)
    # else:
           # return  redirect('/accounts/login/')



@login_required
def add_category(request):
    if request.method == "POST":
        Category(None,request.POST["name"]).save()
        return redirect("/projects/add")


def save_project(request):
    if request.method == "POST":
        try:
            category_id = int(request.POST.get("project_category"))
            category = Category.objects.get(id=category_id)
        except (ValueError, Category.DoesNotExist):

            return HttpResponse("Invalid category ID or category does not exist", status=400)

        if category is None:
            return HttpResponse("Category not found", status=400)

        my_project = Project(
            user=request.user,
            project_title=request.POST["project_title"],
            project_details=request.POST["project_description"],
            total_target=request.POST["project_total_target"],
            start_time=request.POST["project_start_date"],
            end_time=request.POST["project_end_date"],
            category=category,


        )
        my_project.save()

        # Saving project tags
        for tag_name in request.POST.get("project_tags", "").split(" "):
            tag, created = Tags.objects.get_or_create(tag_name=tag_name.strip())
            my_project.tags.add(tag)

        # Saving project images
        for _img in request.FILES.getlist('project_images[]'):
            FileSystemStorage(location='/images')
            Images(project_id=my_project, img=_img).save()

        # Redirect to the project details page
        return redirect(f"/projects/{my_project.id}")
    else:
        # Handle GET request (if applicable)
        return render(request, "user_projects/add_project.html")


def project_details(request, _id):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    # Retrieve the project, but exclude reported projects
    project_data = Project.objects.filter(id=_id, is_reported=False).first()

    if project_data is None:
        return redirect('some_error_page')


    relatedProjects = Project.objects.filter(tags__in=project_data.tags.all()) \
                           .exclude(id=project_data.id) \
                           .annotate(tag_count=Count('tags')) \
                           .order_by('-tag_count')[:4]

    print(relatedProjects)
    print(project_data.id)


    relatedProjects = Project.objects.all().filter(category_id=project_data.category)
    data = project_data
    category = Category.objects.get(id=project_data.category_id)
    total_donate = project_data.donation_set.all().aggregate(Sum('amount'))
    rate_sum = project_data.rate_set.all().aggregate(Sum('rate'))
    rate_count = project_data.rate_set.all().aggregate(Count('rate'))
    tags = project_data.tags.all()

    print(relatedProjects)
    if project_data is None:
        return redirect('some_error_page')

    context = {
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        },
        "data": data,
        "category":category,
        "total_donate": total_donate,
        "rate_sum": rate_sum ,
        "rate_count":rate_count,
        "tags": tags,
        "relatedProjects" :relatedProjects
    }


    return render(request, "user_projects/projectdata.html",context)


def add_comment(request):
    if request.method == "POST":
        project = Project.objects.get(id=request.POST["id"])
        user_id = request.user.id
        Comment(user_id=user_id,project_id=project, content=request.POST["content"]).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def add_reply(request):
    if request.method == "POST":
        comment = Comment.objects.get(id=request.POST["comment_id"])
        user = request.user

        Reply(user=user, comment=comment, content=request.POST["content"]).save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_donation(request):
    project_id = request.POST.get("id")
    amount = request.POST.get("amount")
    
    if project_id and amount:
        project = Project.objects.get(id=project_id)
        user_id = request.user.id  # Fetching user ID from session
        
        # Check if the user has already donated to this project
        donation = Donation.objects.filter(project_id=project, user_id=user_id).first()

        if donation:
            # If user has already donated, update the existing donation amount
            donation.amount += int(amount)
            donation.save()
        else:
            # If user hasn't donated yet, create a new donation record
            Donation.objects.create(project_id=project, user_id=user_id, amount=int(amount))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def rate_project(request):
    if request.method == "POST":
        project = Project.objects.get(id=request.POST["id"])
        user_id = request.user.id
        is_rated = Rate.objects.filter(user_id=user_id,project_id=project)
        if not is_rated:
            Rate(project_id=project,user_id=user_id, rate=request.POST["rate"]).save()
        else:
            Rate.objects.filter(user_id=user_id,project_id=project).update(rate=request.POST["rate"])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def report_comment(request):
    if request.method == "POST":
        print(request.POST, 'fffff')
        comment = Comment.objects.get(id=request.POST["id"])
        user_id = request.user.id
        CommentReports(user_id=user_id,comment_id=comment).save()
        comment.is_reported = True
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def report_project(request ):
    if request.method == "POST":
        # print(request.POST, "sssss")
        project = Project.objects.get(id=request.POST["id"])
        user_id = request.user.id
        ProjectReports(user_id = user_id, project_id=project).save()
        project.is_reported = True
        project.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def user_projects(request, user_id):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    try:
        user = User.objects.get(id=user_id)
        projects = Project.objects.filter(user=user)
        context = {
        "projects": projects,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }
        return render(request, "projects/myprojects.html", {})
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=400)

def user_donations(request, user_id):
    current_user = request.user
    profile = current_user.profile
    user_id = current_user.id
    user_name = current_user.username
    profile_picture = profile.profile_picture
    try:
        user = User.objects.get(id=user_id)
        donations = Donation.objects.filter(user=user)
        context = {
        "donations": donations,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
            
        }
    }
        return render(request, "projects/user_donations.html", context)
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=400)




def some_error_page(request):
    return render(request, 'error_page.html')





def delete_project(request, id):
    if request.method == "POST":
        # Get the project object
        project = get_object_or_404(Project, id=id)
        print(request.user.id)
        # Check if the current user is the owner of the project
        if request.user.id == project.user_id:
            print(request.user)
            # Delete the project
            project.delete()

            return HttpResponseRedirect("/projects/add")
        else:

            return HttpResponseForbidden("Not allowed")
        


# ////////////////////////////////////////////

def project_show(request,id):
    project = get_object_or_404(Project, pk=id)
    return render(request,'user_projects/sliderpase.html',
                  context={'project':project})


def project_edit(request, id):
    project = get_object_or_404(Project, pk=id)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects.index')
    return render(request, 'projects/edit.html', {'form': form, 'project': project})



def project_delete(request, id):
    project = get_object_or_404(Project, pk=id)
    project.delete()
    # return HttpResponse("project deleted")
    return redirect(reverse("projects.index"))









