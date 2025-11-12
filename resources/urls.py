from django.urls import path
from . import views
urlpatterns = [
     path('',views.list_resources,name='resources'),
     path('search/',views.search_resource,name='resource_search'),
     path('delete/<str:id>/',views.delete_resource,name='resource_delete'),
     path('change_status/<str:id>/',views.download_resource,name='resource_download'),

 ]
