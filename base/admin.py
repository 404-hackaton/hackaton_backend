from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(User)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Schedule)
admin.site.register(Grade)
admin.site.register(Attendence)
admin.site.register(Direction)