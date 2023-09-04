from django.urls import path
from .views import lobby


urlpatterns = [
    path("lobby/<room>", lobby, name = "lobby"),
]
