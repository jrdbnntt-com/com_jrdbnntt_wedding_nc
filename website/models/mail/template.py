from django.conf import settings
from django.contrib import admin
from django.db import models

from website.models.mail.subscription_group import EmailSubscriptionGroup


def init():
    """ Does nothing, just here to keep import """
    pass


def default_from_email():
    return settings.EMAIL_FROM_DEFAULT


class EmailTemplate(models.Model):
    """ Email templates """
    name = models.CharField(max_length=100, unique=True)
    from_email = models.CharField(max_length=200, default=default_from_email)
    sendgrid_template_id = models.CharField(max_length=200)
    sendgrid_subscription_group = models.ForeignKey(EmailSubscriptionGroup, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s [sendgrid_template_id='%s', from_email='%s']" % (
            self.name, self.sendgrid_template_id, self.from_email
        )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "subscription_group", "sendgrid_template_id", "from_email")

    @staticmethod
    def subscription_group(obj: EmailTemplate):
        return obj.sendgrid_subscription_group.name if obj.sendgrid_subscription_group is not None else '(none)'
