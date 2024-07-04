from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(Move)
admin.site.register(Following)
admin.site.register(Notification)