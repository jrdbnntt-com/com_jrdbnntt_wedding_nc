from django.db import models
from django.contrib import admin


class FoodOption(models.Model):
    """ Food options for catering """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    picture_url = models.URLField(max_length=200)
    presentation_order = models.IntegerField(default=0)


@admin.register(FoodOption)
class FoodOptionAdmin(admin.ModelAdmin):
    pass
