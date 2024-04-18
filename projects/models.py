from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime
from categories.models import Category





class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project_title = models.CharField(max_length=40)
    project_details = models.TextField(default='')
    total_target = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    category =models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="allprojects")
    project_show = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_reported = models.BooleanField(default=False)

    def __str__(self):
        return self.project_title

    @staticmethod
    def get_all_projects():
        return Project.objects.all()


class Images(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="projects/img")

class Comment(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_reported = models.BooleanField(default=False)





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

class Tags(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.tag_name} for {self.project.project_title}"

class CommentReports(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class ProjectReports(models.Model):
        project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class ReplayComment (models.Model):
    comment_id = models.ForeignKey(Comment , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    comment_content = models.TextField(default=' ')