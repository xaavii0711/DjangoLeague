from django.contrib import admin
from django.urls import path, include

from leagues import views

urlpatterns = [
    path("classificacio",views.classificacio)
]