from django.urls import path
from . import views

urlpatterns = [
    #  path('chapa-webhook/', views.chapa_webhook, name='chapa_webhook'),
    #  path('complete-session/<int:booking_id>/', views.complete_session, name='complete_session'),
    # path('dispute-session/<int:booking_id>/', views.dispute_session, name='dispute_session'),
    # path('auto-complete-sessions/', views.auto_complete_sessions, name='auto_complete_sessions'),
    
    path("success/<str:tx_ref>/", views.payment_success, name="payment_success"),
    path("failed/<str:tx_ref>/", views.payment_failed, name="payment_failed"),
    path("withdraw/", views.withdraw_request, name="withdraw_request"),
 ]