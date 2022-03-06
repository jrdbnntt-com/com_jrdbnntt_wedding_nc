import sendgrid
from json import JSONDecoder, JSONEncoder
import python_http_client
from django.conf import settings

_cached_sendgrid_client = None
json_decoder = JSONDecoder()
json_encoder = JSONEncoder()


def get_sendgrid_client(refresh_cache=False) -> sendgrid.SendGridAPIClient:
    global _cached_sendgrid_client
    if _cached_sendgrid_client is not None and not refresh_cache:
        return _cached_sendgrid_client
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    _cached_sendgrid_client = sg
    return sg


def get_all_results(sg_client: python_http_client,  query_params: dict, page_size=10) -> list[dict]:
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
                raise ValueError('Unable to collect results from json response: %s' % json_encoder.encode(json_response))
        elif isinstance(json_response, list):
            json_results = json_response
            break
    return json_results
