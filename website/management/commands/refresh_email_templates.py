from json import JSONDecoder
from urllib.parse import urlparse, parse_qs

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from website.core.mail import get_sendgrid_client
from website.models.email_template import EmailTemplate


class Command(BaseCommand):
    help = "Retrieves all available SendGrid Dynamic Templates and stores them as EmailTemplate objects"

    def handle(self, *args, **options):
        self.stdout.write('Retrieving SendGrid templates...')
        all_templates = self.get_all_templates()
        self.stdout.write('Got %d SendGrid templates' % len(all_templates))
        if len(all_templates) == 0:
            self.stdout.write('No templates found to refresh, exiting early')
            return

        total_added = 0
        total_updated = 0
        for template in all_templates:
            existed, updated = self.refresh_template(template)
            if existed:
                if updated:
                    total_updated += 1
            else:
                total_added += 1

        self.stdout.write(
            'Successfully added %d new templates and refreshed %s existing templates' % (total_added, total_updated))

    @staticmethod
    def get_all_templates():
        sg = get_sendgrid_client()
        json_decoder = JSONDecoder()
        templates = []
        query_params = {
            'generations': 'dynamic',
            'page_size': 10
        }
        while True:
            templates_resp = sg.client.templates.get(query_params=query_params)
            if templates_resp.status_code != 200:
                raise CommandError(
                    "Received non-200 response from /templates request: %d %s" % templates_resp.status_code,
                    str(templates_resp.body))
            json_response = json_decoder.decode(str(templates_resp.body)[2:-3])
            if len(json_response['result']) > 0:
                for template in json_response['result']:
                    templates.append(template)
            if 'next' in json_response['_metadata']:
                for key, value in parse_qs(urlparse(json_response['_metadata']['next']).query):
                    query_params[key] = value
            else:
                break
        return templates

    @staticmethod
    def refresh_template(template_json: dict) -> tuple[bool, bool]:
        template_name = template_json['name']
        template_id = template_json['id']
        try:
            et = EmailTemplate.objects.filter(name__exact=template_name).get()
            if et.sendgrid_template_id != template_id:
                et.sendgrid_template_id = template_id
                et.save()
                return True, True
            return True, False
        except ObjectDoesNotExist:
            EmailTemplate.objects.create(
                name=template_name,
                sendgrid_template_id=template_id
            )
            return False, True
