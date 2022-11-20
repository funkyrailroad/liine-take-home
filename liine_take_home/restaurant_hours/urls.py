from django.urls import path

from . import views

urlpatterns = [
    path('restaurants', views.TestView.as_view())
]
