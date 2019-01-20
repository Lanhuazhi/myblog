from django.contrib import admin
from blog import models

# Register your models here.
admin.site.register(models.Comment)
admin.site.register(models.Articles)
admin.site.register(models.Group)
admin.site.register(models.Tag)