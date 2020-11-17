from django.contrib import admin
from app import models

admin.site.register(models.Profile)
admin.site.register(models.Rating)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
