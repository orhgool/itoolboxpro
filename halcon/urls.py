from django.urls import path

from . import views

app_name = 'halcon'
urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.IndexView.as_view(), name='index'),
    path('resultados/', views.resultados, name='resultados'),
    path('<int:url_id>/detalle/', views.detalle, name='detalle'),
]