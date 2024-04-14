from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images', blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'