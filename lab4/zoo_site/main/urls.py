from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^animals/$', views.animals, name='animals'),
    re_path(r'^placements/$', views.placements, name='placements'),
]