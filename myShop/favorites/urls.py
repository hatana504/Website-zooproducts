from django.urls import path

from . import views

urlpatterns = [
    path('', views.favorites_list, name='favorites_list'),
    path('add/', views.favorites_add, name='favorites_add'),
    path('remove/', views.favorites_remove, name='favorites_remove'),
    path('remove/<id>', views.favorites_list_remove, name='favorites_list_remove'),
    path('api/', views.favorites_api, name='favorites_api'),
]
