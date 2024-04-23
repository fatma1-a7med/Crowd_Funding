from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from categories.models import Category
from django.shortcuts import reverse
from django.shortcuts import get_list_or_404



class Tags(models.Model):
    tag_name = models.CharField(max_length=40)

    def __str__(self):
        return self.tag_name


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='superuser_projects')
    project_title = models.CharField(max_length=40)
    project_details = models.TextField(default='')
    total_target = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="superuser_projects")
    project_show = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_reported = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    img = models.ImageField(upload_to= "projects/img", null=True, blank=True)


    def __str__(self):
        return self.project_title

    @property
    def show_url(self):
        return reverse('projectDetails', args=[self.id])

    @staticmethod
    def get_all_projects():
        return Project.objects.all()

    @staticmethod
    def get_featured_projects():
        return Project.objects.filter(featured=True).order_by('-created_at')[:5]

class Images(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_images')
    img = models.ImageField(upload_to="projects/img")

    @property
    def image_url(self):
        return f"/media/{self.img}"


class Comment(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_comments')
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='superuser_comments')
    is_reported = models.BooleanField(default=False)


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superuser_replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    rate = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_rates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='superuser_rates')


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='superuser_donations')
    amount = models.IntegerField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_donations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} for {self.project.project_title}"


class CommentReports(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='superuser_comment_reports')


class ProjectReports(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='superuser_project_reports')



## category models ##

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True )
    description = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return f"{self.name}"
    


    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    


    @property
    def logo_url(self):
      return f"/media/{self.logo}"  
    

    @staticmethod
    def get_category_by_id(id):
     return get_list_or_404(Category, pk=id)

    
    @property
    def index_url(self):
     return reverse("categories_index", args= [self.id]) 
    
    @property
    def show_url(self):
     return reverse("categories_show", args= [self.id])    
    
    @property
    def delete_url(self):
     return reverse('category_delete', args=[self.id])  
    

    @property
    def edit_url(self):
     return reverse('category_edit', args=[self.id])
    


