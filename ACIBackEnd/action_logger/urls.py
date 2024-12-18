from django.urls import path
from django.urls import include

from action_logger.views import hello_world

HELLO_WORLD_TEST = "hello_world_test"

urlpatterns = [
    path("hello/world/", hello_world, name=HELLO_WORLD_TEST),


]
