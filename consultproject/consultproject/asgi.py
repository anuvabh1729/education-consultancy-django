"""
ASGI config for consultproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# PROJECT ROOT: consultproject/asgi.py  (REQUIRED for WebSockets)
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatbox.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consultproject.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
