from django.urls import path
from . import views

urlpatterns = [ 
    path("success/<str:tx_ref>/", views.payment_success, name="payment_success"),
    path("failed/<str:tx_ref>/", views.payment_failed, name="payment_failed"),
    path("withdraw/", views.withdraw_request, name="withdraw_request"),
 ]