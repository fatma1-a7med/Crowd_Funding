from django.contrib import admin
from .models import *

# Define custom admin actions
def mark_as_featured(modeladmin, request, queryset):
    selected_project_count = queryset.count()
    if selected_project_count > 5:
        modeladmin.message_user(request, "You can only select up to 5 projects as featured.", level='ERROR')
    else:
        queryset.update(featured=True)

mark_as_featured.short_description = "Mark selected projects as featured (max 5)"

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'project_details', 'featured']
    list_editable = ['featured']
    actions = [mark_as_featured]

mark_as_featured.short_description = "Mark selected projects as featured (max 5)"


# Register models and admin classes
admin.site.register(Project,ProjectAdmin)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(Donation)
admin.site.register(Rate)
admin.site.register(CommentReports)
admin.site.register(ProjectReports)
