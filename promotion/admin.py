from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(post)
admin.site.register(Media)
admin.site.register(News)
admin.site.register(Event)