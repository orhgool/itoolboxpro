from django.urls import path

from . import views

app_name = 'halcon'
urlpatterns = [
    path('', views.index, name='index'),
]