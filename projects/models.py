from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Project(models.Model):
    title=models.CharField(max_length=100)
    details = models.TextField(max_length=2000)
    totaltarget = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

class Category(models.Model):
    name = models.CharField(max_length=50)
    cat_image = models.ImageField(upload_to='static/imgs/' ,default=True)



    def __str__(self):
        return str(self.title)

class Pictures(models.Model):
    img_url = models.ImageField(upload_to='static/imgs' , verbose_name='Image' )
    project = models.ForeignKey(Project , on_delete=models.CASCADE , default=None ,related_name='imgs')

    def __str__(self):
        return str(self.project.title)

class Comment(models.Model):
    content = models.TextField(max_length=200 , blank=False)
    project = models.ForeignKey("Project" , on_delete=models.CASCADE)
    # user = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(f'comment by {self.user.username} on {self.project.title} project.')

class CommentReport(models.Model):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    # user = models.ForeignKey(users)

class ProjectReport(models.Model):
     content = models.TextField(max_length=2000)
     project = models.ForeignKey("Project",on_delete=models.CASCADE)
     #user = models.ForeignKey("users")

     def __str__(self):
         return f" {self.user.first_name} {self.user.last_name} on report {self.project.title} "

class Rate(models.Model):

    value = models.IntegerField(validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ]);
    project = models.ForeignKey("Project" , on_delete=models.CASCADE)
    #user = models.ForeignKey()

class Donation(models.Model):
    amount = models.IntegerField()
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    # user = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return (f"{self.user} Donate to {self.project}")
