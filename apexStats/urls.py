from django.urls import path

from . import views

app_name = 'apex'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('results', views.tracker_results, name='results'),
]
