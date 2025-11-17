from django.urls import path
from . import views
urlpatterns = [
     path('create/<int:session_id>/', views.create_virtual_class, name='create_virtual_class'), 
    path('join/<str:session_id>/', views.join_virtual_class, name='join_virtual_class'),    path('check_in_out/<int:session_id>/', views.check_in_out, name='check_in_out'),
    path('check_in_out/<int:session_id>/', views.check_in_out, name='check_in_out'),
 
]
