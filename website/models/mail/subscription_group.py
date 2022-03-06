from django.conf import settings
from django.contrib import admin
from django.db import models


class EmailSubscriptionGroup(models.Model):
    """ Email Subscription Groups """
    sendgrid_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@admin.register(EmailSubscriptionGroup)
class EmailSubscriptionGroupAdmin(admin.ModelAdmin):
    list_display = ("sendgrid_id", "name", "description")
