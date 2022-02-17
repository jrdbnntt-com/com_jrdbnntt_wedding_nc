from django.core.exceptions import ValidationError
from django.http import HttpRequest
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

MIN_RECAPTCHA_SCORE = 0.1 if settings.DEBUG else 0.5

# reCAPTCHA actions to use
RECAPTCHA_ACTION_SIGN_IN_USER = "sign_in_user"
RECAPTCHA_ACTION_SIGN_IN_RESERVATION = "sign_in_reservation"


class RecaptchaCheckError(Exception):
    pass


class RecaptchaCheckResponse:
    def __init__(self, json):
        json = dict(json)
        self.success = bool(json['success'])
        self.score = float(json['score'])
        self.action = str(json['action'])
        self.hostname = str(json['hostname'])
        if 'error-codes' in json:
            self.error_codes = list(json['error-codes'])
        else:
            self.error_codes = []


def validate_recaptcha_token(request: HttpRequest, token: str, action: str):
    if action is None or action == "":
        raise ValueError("action required")
    try:
        if token is None or token == "":
            raise ValidationError("token missing")

        # Verify the token with Google
        try:
            resp = requests.post("https://www.google.com/recaptcha/api/siteverify", {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': token
            })
        except Exception as e:
            raise RecaptchaCheckError("reCAPTCHA verify request failed") from e
        if resp.status_code != 200:
            raise RecaptchaCheckError("reCAPTCHA verify request returned bad status code '{}'".format(resp.status_code))
        try:
            verify_response = RecaptchaCheckResponse(resp.json())
        except Exception as e:
            raise RecaptchaCheckError("failed to read recaptcha verify response as json (response='{}')".format(resp.raw)) from e

        # Validate the attempt based on Google's verify response
        if len(verify_response.error_codes) != 0:
            raise ValidationError('reCAPTCHA verify returned with errors: {}'.format(verify_response.error_codes))
        if not verify_response.success:
            raise ValidationError('invalid recaptcha token')
        if verify_response.score < MIN_RECAPTCHA_SCORE:
            raise ValidationError('reCAPTCHA verify score ({}) lower than the minimum required score ({})'.format(verify_response.score, MIN_RECAPTCHA_SCORE))
        if verify_response.action != action:
            raise ValidationError("reCAPTCHA token expected for action '{}', but token's action was '{}'".format(action, verify_response.action))

        request_host = request.get_host()
        if ":" in request_host:
            request_host = request_host.split(':')[0]
        if verify_response.hostname != request_host:
            raise ValidationError("reCAPTCHA token not evaluated from the same host ({}) as request ({})".format(verify_response.hostname, request_host))

    except ValidationError as e:
        raise ValidationError('reCAPTCHA check failed') from e
    except RecaptchaCheckError as e:
        # Log the unexpected error but still return the same generic message
        logger.error(e, exc_info=True)
        raise ValidationError('reCAPTCHA check failed') from e
    except Exception as e:
        # Wrap and log the unexpected error but still return the same generic message
        try:
            raise RecaptchaCheckError("unexpected error when checking reCAPTCHA") from e
        except RecaptchaCheckError as e:
            logger.error(e, exc_info=True)
        raise ValidationError('reCAPTCHA check failed') from e
