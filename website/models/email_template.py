from django.conf import settings
from django.contrib import admin
from django.db import models


def default_from_email():
    return settings.EMAIL_FROM_DEFAULT


class EmailTemplate(models.Model):
    """ Email templates """
    name = models.CharField(max_length=100, unique=True)
    sendgrid_template_id = models.CharField(max_length=200)
    from_email = models.CharField(max_length=200, default=default_from_email)

    def __str__(self):
        return "%s [sendgrid_template_id='%s', from_email='%s']" % (
            self.name, self.sendgrid_template_id, self.from_email
        )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "sendgrid_template_id", "from_email")
