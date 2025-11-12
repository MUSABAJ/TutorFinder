from django.urls import path
from .views import admin_stats_view

urlpatterns = [
    path('',admin_stats_view, name='admin_stats_view')
]