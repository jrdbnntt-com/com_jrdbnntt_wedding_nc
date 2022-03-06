from django.db import models
from django.contrib import admin


class EmailTemplate(models.Model):
    """ Email templates """
    name = models.CharField(max_length=100, unique=True)
    sendgrid_template_id = models.CharField(max_length=200)
    from_email = models.CharField(max_length=200)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    pass
