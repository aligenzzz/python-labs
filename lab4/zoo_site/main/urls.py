from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('animals/', views.AnimalListView.as_view(), name='animals'),
    path('animals/<int:id>/', views.AnimalDetailsView.as_view(), name='animal'),
    path('placements/', views.PlacementListView.as_view(), name='placements'),
    path('placements/<int:id>/', views.PlacementDetailsView.as_view(), name='placement'),
    path('placements/<int:id>/animals/', views.PlacementAnimalsView.as_view(), name='placement_animals'),
    path('staff/', views.StafferListView.as_view(), name='staff'),
    path('staff/<int:id>/', views.StafferDetailsView.as_view(), name='staffer'),
    path('staff/<int:id>/animals', views.StafferAnimalsView.as_view(), name='staffer_animals'),
    path('staff/<int:id>/placements', views.StafferPlacementsView.as_view(), name='staffer_placements'),
]