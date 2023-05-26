from django.urls import path
from . import views

urlpatterns = [

    path("rest/v1/calendar/init", views.google_auth),
    path("rest/v1/calendar/redirect/", views.google_auth_callback)

]
