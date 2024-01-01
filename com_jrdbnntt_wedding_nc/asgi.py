"""
ASGI config for com_jrdbnntt_wedding_nc project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'com_jrdbnntt_wedding_nc.settings')

application = get_asgi_application()
