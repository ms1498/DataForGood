from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("showStats", views.showStats, name="showStats"),
    path("calculate", views.calculateRiskPage, name="calculateRiskPage"),
]