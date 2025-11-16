from django.urls import path
from . import views
urlpatterns = [
    path('tutor_register/', views.tutor_register, name='tutor_register'),
    path('student_register/', views.student_register, name='student_register'),
    path('payment_method/', views.payment_info_form, name='payment_info_form'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
 ]
