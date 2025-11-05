from django.urls import path
from . import views

urlpatterns = [
    path('form/<int:session_id>/', views.give_feedback, name='give_feedback'),
    path('list/', views.feedback_list, name='feedback_list'),
    path('detail/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
]
