from django.contrib import admin
from .models import Images, Comment, Reply, Rate, Donation, CommentReports, ProjectReports, Tags

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1


class RateInline(admin.TabularInline):
    model = Rate
    extra = 1


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 1


class TagsInline(admin.TabularInline):
    model = Tags.project_set.through
    extra = 1


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'content', 'created_at', 'user', 'is_reported')
    list_filter = ('created_at', 'is_reported')
    search_fields = ['project_id__project_title', 'user__username']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'content', 'timestamp')
    search_fields = ['comment__content', 'user__username']


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_id', 'rate')
    search_fields = ['project_id__project_title', 'user__username']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'project_id', 'created_at')
    search_fields = ['project_id__project_title', 'user__username']


@admin.register(CommentReports)
class CommentReportsAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user')
    search_fields = ['comment_id__content', 'user__username']


@admin.register(ProjectReports)
class ProjectReportsAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'user')
    search_fields = ['project_id__project_title', 'user__username']
