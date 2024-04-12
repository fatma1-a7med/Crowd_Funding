from django.shortcuts import render ,redirect ,reverse , get_object_or_404
from .models import *
from .forms  import ProjectForm,ImageForm
from django.forms import modelformset_factory
from django.db.models import Q , Avg , Sum
from decimal import Decimal, ROUND_HALF_UP
from taggit.models import Tag
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

# def showProject(request , id):
#    project = Project.objects.get(id = id)
#    relatedProjects = Project.objects.all().filter(category_id = project.category)
#    projectpics = Pictures.objects.all().filter(project_id = id)
#    rate = project.rate_set.all().aggregate(Avg("value"))["value__avg"]
#    rate = rate if rate else 0
#    rate = Decimal(rate).quantize(0,ROUND_HALF_UP)
#    start_date = project.start_date
#    end_date = project.end_date

from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Sum

def showProject(request, id):
    item = get_object_or_404(Project.objects.prefetch_related('projectpicture_set', 'rate_set', 'donation_set'), id=id)
    pPics = item.projectpicture_set.all()
    relatedProjects = Project.objects.filter(category=item.category).exclude(id=id).order_by('-created_at')[:4]
    rate = item.rate_set.all().aggregate(Avg("value"))["value__avg"]
    rate = rate if rate else 0
    rate = Decimal(rate).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
    now = timezone.now()
    start_date = item.start_date
    end_date = item.end_date
    donate = item.donation_set.all().aggregate(Sum("amount"))
    context = {'pData': item,
               'pPics': pPics,
               'rate': rate,
               'now': now,
               'start_date': start_date,
               'end_date': end_date,
               'relatedProjs': relatedProjects,
               'donations_amount': donate["amount__sum"] if donate["amount__sum"] else 0}
    if request.user.is_authenticated:
        user_rate = item.rate_set.filter(user=request.user.profile).first()
        if user_rate:
            context["user_rate"] = user_rate.value
    return render(request, "projects/viewProject.html", context)


def createProject(request):
   ImageFormSet = modelformset_factory(Pictures, form=ImageForm, min_num=1, extra=3)

   if request.method == 'POST':
      form = ProjectForm(request.POST)
      formset = ImageFormSet(request.POST, request.FILES, queryset=Pictures.objects.none())

      if form.is_valid() and formset.is_valid():
         new_project = form.save(commit=False)
         new_project.save()
         form.save_m2m()
         for image_form in formset.cleaned_data:
            if image_form:
               image = image_form['img_url']
               photo = Pictures(project=new_project, img_url=image)
               photo.save()
         return redirect(f'/projects/projectDetails/{new_project.id}')
   else:
      form = ProjectForm()
      formset = ImageFormSet(queryset=Pictures.objects.none())

   context = {
      'form': form,
      'formset': formset,
   }
   return render(request, 'projects/create.html', context)







