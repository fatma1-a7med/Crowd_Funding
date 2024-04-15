from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(Donation)
admin.site.register(Rate)
admin.site.register(CommentReports)
admin.site.register(ProjectReports)

admin.site.register(Category)


