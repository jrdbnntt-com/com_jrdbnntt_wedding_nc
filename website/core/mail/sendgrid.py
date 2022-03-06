import json
import logging
from json import JSONDecoder, JSONEncoder

import python_http_client
import sendgrid
from django.conf import settings
from django.core.mail import EmailMessage

from website.models.mail.template import EmailTemplate

logger = logging.getLogger(__name__)
_cached_sendgrid_client = None
json_decoder = JSONDecoder()
json_encoder = JSONEncoder()


def get_template(name: str) -> EmailTemplate:
    template = EmailTemplate.objects.filter(name__exact=name).get()
    if template.sendgrid_subscription_group is None:
        logger.warning("Email template '%s' does not have subscription group" % template.sendgrid_subscription_group)
    return template


def send_dynamic_template_email(template_name: str, to_email: str, dynamic_template_data: dict):
    template = get_template(template_name)
    msg = EmailMessage(
        from_email=template.from_email,
        to=[to_email]
    )
    msg.template_id = template.sendgrid_template_id
    msg.dynamic_template_data = dynamic_template_data
    if template.sendgrid_subscription_group is not None:
        msg.asm = {
            'group_id': template.sendgrid_subscription_group.sendgrid_id
        }
    try:
        msg.send()
    except Exception as e:
        logger.warning("Failed to send '%s' email to '%s' with data '%s': %s" % (
            template_name,
            to_email,
            json.dumps(dynamic_template_data),
            e
        ))


def get_sendgrid_client(refresh_cache=False) -> sendgrid.SendGridAPIClient:
    global _cached_sendgrid_client
    if _cached_sendgrid_client is not None and not refresh_cache:
        return _cached_sendgrid_client
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    _cached_sendgrid_client = sg
    return sg


def get_all_results(sg_client: python_http_client, query_params: dict, page_size=10) -> list[dict]:
    json_results = []
    if page_size is not None:
        query_params['page_size'] = page_size
    while True:
        resp = sg_client.get(query_params=query_params)
        json_response = json_decoder.decode(str(resp.body)[2:-3])
        if isinstance(json_response, dict):
            if 'result' in json_response:
                if len(json_response['result']) > 0:
                    for result in json_response['result']:
                        json_results.append(result)
                if '_metadata' in json_response and 'next' in json_response['_metadata']:
                    for key, value in parse_qs(urlparse(json_response['_metadata']['next']).query):
                        query_params[key] = value
                else:
                    break
            else:
                raise ValueError(
                    'Unable to collect results from json response: %s' % json_encoder.encode(json_response))
        elif isinstance(json_response, list):
            json_results = json_response
            break
    return json_results
