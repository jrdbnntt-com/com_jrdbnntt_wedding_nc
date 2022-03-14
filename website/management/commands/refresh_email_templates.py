from urllib.parse import urlparse, parse_qs

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from website.models.mail.template import EmailTemplate
from website.models.mail.subscription_group import EmailSubscriptionGroup
from website.core.mail import sendgrid


class Command(BaseCommand):
    help = "Retrieves all available SendGrid Dynamic Templates and stores them as EmailTemplate objects"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.sendgrid = sendgrid.get_sendgrid_client()

    def handle(self, *args, **options):
        self.refresh_all_templates()
        self.refresh_all_subscription_groups()

    def refresh_all_templates(self):
        self.stdout.write('Retrieving SendGrid templates...')
        all_templates = self.get_all_templates()
        self.stdout.write('Got %d SendGrid templates' % len(all_templates))
        if len(all_templates) == 0:
            self.stdout.write('No templates found to refresh')
            return
        total_added = 0
        total_updated = 0
        for template in all_templates:
            new, updated = self.refresh_template(template)
            if new:
                total_added += 1
            if updated:
                total_updated += 1
        self.stdout.write(
            'Successfully added %d new and refreshed %s existing EmailTemplates' % (total_added, total_updated))

    def refresh_all_subscription_groups(self):
        self.stdout.write('Retrieving SendGrid subscription groups...')
        all_groups = self.get_all_subscription_groups()
        self.stdout.write('Got %d SendGrid subscription groups' % len(all_groups))
        if len(all_groups) == 0:
            self.stdout.write('No SendGrid subscription groups to found to refresh')
            return
        total_added = 0
        total_updated = 0
        for template in all_groups:
            new, updated = self.refresh_subscription_group(template)
            if new:
                total_added += 1
            if updated:
                total_updated += 1
        self.stdout.write(
            'Successfully added %d new and refreshed %s existing EmailSubscriptionGroups' % (total_added, total_updated))

    def get_all_templates(self):
        return sendgrid.get_all_results(self.sendgrid.client.templates, {
            'generations': 'dynamic'
        })

    def get_all_subscription_groups(self):
        return sendgrid.get_all_results(self.sendgrid.client.asm.groups, query_params={})

    @staticmethod
    def refresh_template(template_json: dict) -> tuple[bool, bool]:
        template_name = template_json['name']
        template_id = template_json['id']
        try:
            et = EmailTemplate.objects.filter(name__exact=template_name).get()
            if et.sendgrid_template_id != template_id:
                et.sendgrid_template_id = template_id
                et.save()
                return False, True
            return False, False
        except ObjectDoesNotExist:
            EmailTemplate.objects.create(
                name=template_name,
                sendgrid_template_id=template_id
            )
            return True, False

    @staticmethod
    def refresh_subscription_group(group_json: dict) -> tuple[bool, bool]:
        name = group_json['name']
        sendgrid_id = group_json['id']
        description = group_json['description']
        try:
            group = EmailSubscriptionGroup.objects.filter(sendgrid_id=sendgrid_id).get()
            updated = False
            if group.name != name:
                group.name = name
                updated = True
            if group.description != group.description:
                group.description = description
                updated = True
            if updated:
                group.save()
            return False, updated
        except ObjectDoesNotExist:
            EmailSubscriptionGroup.objects.create(
                name=name,
                sendgrid_id=sendgrid_id,
                description=description
            )
            return True, False


