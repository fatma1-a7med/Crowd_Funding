from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime
from categories.models import Category
from django.shortcuts import reverse


class Tags(models.Model):

    tag_name = models.CharField(max_length=40)

    def __str__(self):
        return self.tag_name

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project_title = models.CharField(max_length=40)
    project_details = models.TextField(default='')
    total_target = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="allprojects")
    project_show = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_reported = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.project_title

    @property
    def show_url(self):
        return reverse('projectDetails', args=[self.id])

    @staticmethod
    def get_all_projects():
        return Project.objects.all()


class Images(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="projects/img")

    @property
    def image_url(self):
        return f"/media/{self.image}"


class Comment(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_reported = models.BooleanField(default=False)

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Rate(models.Model):
    rate = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} for {self.project.project_title}"


class CommentReports(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class ProjectReports(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


