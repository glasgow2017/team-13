from django.contrib import admin
from .models import UserProfile, Request, Call

admin.site.register(UserProfile)
admin.site.register(Request)
admin.site.register(Call)
