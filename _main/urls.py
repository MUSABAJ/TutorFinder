from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('', include('core.urls')),
    path('sessions/', include('tutor_sessions.urls')),
    path('availablity/',include('availablity.urls')),
    path('payment/',include('payments.urls')),
    path('chats/',include('chat.urls')),
    path('feedback/session/', include('feedback.urls')),
    path('resources/', include('resources.urls')),


]
