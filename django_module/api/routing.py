from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/funding/", consumers.FundingConsumer.as_asgi()),
]
