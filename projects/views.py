from django.db import models
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg, Sum,F
from .models import *




def perojects_index(request):
    projects = Project.get_all_projects()
    return render(request,'user_projects/allprojects.html',
                  context={'projects':projects})
def add_project(request):
     # if 'id' in request.session:
      return render(request,"user_projects/add_project.html",{"categories" : Category.objects.all()})
     # else:
     #   return  redirect('/login')


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
            category=category
        )
        my_project.save()

        # Saving project tags
        for tag in request.POST.get("project_tags", "").split(","):
            Tags.objects.create(project=my_project, tag_name=tag.strip())

        # Saving project images
        for _img in request.FILES.getlist('project_images[]'):
            FileSystemStorage(location='/images')
            Images(project_id=my_project, img=_img).save()

        # Redirect to the project details page
        return redirect(f"/projects/{my_project.id}")
    else:
        # Handle GET request (if applicable)
        return render(request, "user_projects/add_project.html")


# def project_details(request, _id):
#     # if 'id' in request.session:
#     #     print('mwgooooookokokokokokokd')
#         project_data = Project.objects.get(id=_id)
#         project_category = Category.objects.get(id=project_data.category_id)
#         project = {"data": project_data, "category": project_category,
#                    "total_donate": project_data.donation_set.all().aggregate(Sum('amount')),
#                    "rate_sum": project_data.rate_set.all().aggregate(Sum('rate')),
#                    "rate_count": project_data.rate_set.all().aggregate(Count('rate'))}
#
#         return render(request, "user_projects/sliderpase.html", project)
#
#     # else:
#         print('sssssssssss')
#         return redirect('/login')
def project_details(request, _id):
    # Retrieve the project, but exclude reported projects
    project_data = Project.objects.filter(id=_id, is_reported=False).first()

    if project_data is None:

        return redirect('some_error_page')

    project_category = Category.objects.get(id=project_data.category_id)
    project = {"data": project_data, "category": project_category,
               "total_donate": project_data.donation_set.all().aggregate(Sum('amount')),
               "rate_sum": project_data.rate_set.all().aggregate(Sum('rate')),
               "rate_count": project_data.rate_set.all().aggregate(Count('rate'))}

    return render(request, "user_projects/sliderpase.html", project)


def add_comment(request):
    if request.method == "POST":
        project = Project.objects.get(id=request.POST["id"])
        user_id = request.user.id
        Comment(user_id=user_id,project_id=project, content=request.POST["content"]).save()
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
    try:
        user = User.objects.get(id=user_id)
        projects = Project.objects.filter(user=user)
        return render(request, "projects/myprojects.html", {"projects": projects})
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=400)

def user_donations(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        donations = Donation.objects.filter(user=user)

        for donation in donations:
            print(f"Donation ID: {donation.id}, Amount: {donation.amount}, Project: {donation.project_id.project_title}, Date: {donation.created_at}")

        return render(request, "projects/user_donations.html", {"donations": donations})
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=400)




def some_error_page(request):
    return render(request, 'error_page.html')



def delete_project(request):
    if request.method == "POST":
        Project.objects.filter(id=request.POST["id"]).delete()
        return HttpResponseRedirect("/projects/add")


# def home(req):
#     latest_project = Project.objects.order_by('-created_at')[:5]
#     # print("Latest Projects:", latest_project)  # Add this line for debugging
#     return render(req, 'index.html', context={'projects': latest_project})

