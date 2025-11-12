
from django.urls import path
from . import views
urlpatterns = [

    path('list/', views.notification_list, name='notification'),
    path('mark_read/', views.mark_notification_read, name='mark_read'),
 
]
