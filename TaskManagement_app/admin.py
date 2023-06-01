from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHR, TeamHead, TeamMem, Project,Task,LeaveReport,FeedBack

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHR)
admin.site.register(TeamHead)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TeamMem)
admin.site.register(FeedBack)
admin.site.register(LeaveReport)


# Register your models here.
