from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('asset/add/', views.asset_create, name='asset_create'),
    path('asset/<int:pk>/', views.asset_detail, name='asset_detail'),
    path('asset/<int:pk>/edit/', views.asset_edit, name='asset_edit'),
    path('asset/<int:pk>/delete/', views.asset_delete, name='asset_delete'),
]
