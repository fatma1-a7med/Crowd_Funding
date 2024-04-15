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


def add_project(request):
    # // if 'id' in request.session:

        return render(request,"user_projects/add_project.html", {"categories" : Category.objects.all()})
     # else:
     #    return  redirect('/login')


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
            # Handle invalid category ID or missing category
            # You might want to return an error response or redirect to a different page
            # For now, I'll just return a generic error response
            return HttpResponse("Invalid category ID or category does not exist", status=400)

        if category is None:
            # Handle case where category is not found
            return HttpResponse("Category not found", status=400)

        my_project = Project(
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


def project_details(request, _id):
    # if 'id' in request.session:
    #     print('mwgooooookokokokokokokd')
        project_data = Project.objects.get(id=_id)
        project_category = Category.objects.get(id=project_data.category_id)
        project = {"data": project_data, "category": project_category,
                   "total_donate": project_data.donation_set.all().aggregate(Sum('amount')),
                   "rate_sum": project_data.rate_set.all().aggregate(Sum('rate')),
                   "rate_count": project_data.rate_set.all().aggregate(Count('rate'))}

        return render(request, "user_projects/sliderpase.html", project)

    # else:
        print('sssssssssss')
        return redirect('/login')


def add_comment(request):
    if request.method == "POST":
        project = Project.objects.get(id=request.POST["id"])
        # user = User.objects.get(id=request.session['id'])
        Comment(project_id=project, content=request.POST["content"]).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_donation(request):
    project = Project.objects.get(id=request.POST["id"])
    # user = User.objects.get(id=request.session['id'])
    is_donated = Donation.objects.filter( project_id=project)
    if not is_donated:
        Donation( project_id=project, amount=request.POST["amount"]).save()
    else:
        Donation.objects.filter(project_id=project).update(
            amount=F("amount") + request.POST["amount"])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def rate_project(request):
    if request.method == "POST":
        project = Project.objects.get(id=request.POST["id"])
        #user = User.objects.get(id=request.session['id'])
        is_rated = Rate.objects.filter(id=project)
        if not is_rated:
            Rate(id=project, rate=request.POST["rate"]).save()
        else:
            Rate.objects.filter(id=project).update(rate=request.POST["rate"])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def report_comment(request):
    if request.method == "POST":
        print(request.POST, 'fffff')
        comment = Comment.objects.get(id=request.POST["id"])
        # user = User.objects.get(id=request.session["id"])
        CommentReports(comment_id=comment).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def report_project(request):
    if request.method == "POST":
        print(request.POST, "sssss")
        project = Project.objects.get(id=request.POST["id"])
        # user = User.objects.get(id=request.session["id"])
        ProjectReports(project_id=project).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
