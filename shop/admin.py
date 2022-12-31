from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(User1)
admin.site.register(subscriptions)
admin.site.register(positions_userwise)
admin.site.register(positions)
admin.site.register(UserOTP)