from django.urls import path

from . import views

urlpatterns = [
    path('run', views.index, name='index'),
    path('check', views.status_last, name='status_last'),
    path('info', views.get_info, name='get_info'),
    path('details', views.get_info_details, name='get_info_details'),
    path('chart', views.get_chart, name='get_chart'),
    path('available', views.available_runs, name='available_runs'),
]