from django.shortcuts import render
from django.db.models import Max
from projects.models import Project
from home.forms import ProjectSearchForm
from categories.models import Category
from projects.models import Rate

def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        profile = current_user.profile
        user_id = current_user.id
        user_name = current_user.username
        profile_picture = profile.profile_picture
    else:
        profile = None
        user_id = None
        user_name = None
        profile_picture = None

    form = ProjectSearchForm()
    search_results = []
    category_results = None
    tag_results = None
    featured_projects = Project.objects.filter(featured=True).order_by('-created_at')[:5]
    latest_project = Project.objects.order_by('-created_at')[:5]
    highest_rated_projects = Rate.objects.values('project_id').annotate(max_rate=Max('rate')).order_by('-max_rate')[:5]
    highest_rated_project_ids = [record['project_id'] for record in highest_rated_projects]
    top_rated_projects = Project.objects.filter(id__in=highest_rated_project_ids)

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
                if tag_results.exists():
                    search_results = tag_results
    context = {
        'projects': latest_project,
        'featured_projects': featured_projects,
        'search_results': search_results,
        'tag_results': tag_results, 
        'top_rated_projects': top_rated_projects,
        'userData': {
            'user_id': user_id,
            'username': user_name,
            'profile_picture': profile_picture,
        }
    }            
    return render(request, 'home/index.html', context=context)
