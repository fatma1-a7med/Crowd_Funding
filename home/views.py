from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from projects.models import *
# from categories.models import *
from home.forms import ProjectSearchForm



# Create your views here.

from django.db.models import Q

def home(req):
    form = ProjectSearchForm()
    search_results = []
    category_results = None 
    featured_projects = Project.objects.filter(featured=True).order_by('-created_at')[:5]
    latest_project = Project.objects.order_by('-created_at')[:5]
    query = req.GET.get('query')
    
    if query:
        category_results = Category.objects.filter(name__icontains=query)
        if category_results is not None and category_results.exists():
            category = category_results.first()
            search_results = Project.objects.filter(category=category)
        else:
            # Handle the case when no categories match the query
            search_results = []  # Assign an empty list to search_results
    else:
        # Handle the case when no query is provided
        search_results = [] 
    return render(req, 'home/index.html', context={'projects': latest_project, 'featured_projects': featured_projects, 'search_results' : search_results})
