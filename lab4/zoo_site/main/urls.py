from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('animals/', views.AnimalListView.as_view(), name='animals'),
    path('animals/<int:id>/', views.AnimalDetailsView.as_view(), name='animal'),
    path('placements/', views.PlacementListView.as_view(), name='placements'),
    path('placements/<int:id>/', views.PlacementDetailsView.as_view(), name='placement'),
    path('placements/<int:id>/animals/', views.PlacementAnimalsView.as_view(), name='placement_animals'),
    path('staff/', views.StafferListView.as_view(), name='staff'),
    path('staff/<int:id>/', views.StafferDetailsView.as_view(), name='staffer'),
    path('staff/<int:id>/animals/', views.StafferAnimalsView.as_view(), name='staffer_animals'),
    path('staff/<int:id>/placements/', views.StafferPlacementsView.as_view(), name='staffer_placements'),
    path('personal/', views.PersonalAccountView.as_view(), name='personal_account'),
    path('personal/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('personal/animals/', views.UserAnimalsView.as_view(), name='user_animals'),
    path('personal/placements/', views.UserPlacementsView.as_view(), name='user_placements'),
    path('personal/settings/', views.UserSettingsView.as_view(), name='user_settings'),
]