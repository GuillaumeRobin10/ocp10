from django.contrib import admin
from .models import Projects, Contributors, Issues, Comments

"""class UserFollowAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")
    """


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', "title", "description")


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("user_id", "project_id", "role")


class IssuesAdmin(admin.ModelAdmin):
    list_display = ("title", "desc", "tag",
                    "priority", "project_id", "status",
                    "author_user_id", "assignee_user_id", "created_time")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("description", "author_user_id", "issue_id",
                    "created_time")


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Contributors, ContributorAdmin)
admin.site.register(Issues, IssuesAdmin)
admin.site.register(Comments, CommentsAdmin)
