from django.urls import path
from .views import inicio

app_name = "hotel"

urlpatterns = [
    path("", inicio, name="inicio"),
]