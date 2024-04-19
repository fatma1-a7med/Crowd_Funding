from django.shortcuts import render
from django.db.models import Max
from projects.models import Project
from home.forms import ProjectSearchForm
from categories.models import Category
from projects.models import Rate

def home(request):
    form = ProjectSearchForm()
    search_results = []
    category_results = None
    tag_results = None
    featured_projects = Project.objects.filter(featured=True).order_by('-created_at')[:5]
    latest_project = Project.objects.order_by('-created_at')[:5]
    highest_rated_project_id = Rate.objects.values('project_id').annotate(max_rate=Max('rate')).order_by('-max_rate').first()

    if highest_rated_project_id:
        highest_rated_project = Project.objects.get(id=highest_rated_project_id['project_id'])
    else:
        highest_rated_project = None

    query = request.GET.get('query')
    
    if query:
        # Search by category name
        category_results = Category.objects.filter(name__icontains=query)
        if category_results.exists():
            category = category_results.first()
            search_results = Project.objects.filter(category=category)
        else:
            # Search by project title
            search_results = Project.objects.filter(project_title__icontains=query)
            if not search_results.exists():
                # Search by tag name
                tag_results = Project.objects.filter(tags__tag_name__icontains=query)

    return render(request, 'home/index.html', {
        'projects': latest_project,
        'featured_projects': featured_projects,
        'search_results': search_results,
        'tag_results': tag_results,  # Include tag search results in the context
        'highest_rated_project': highest_rated_project
    })
