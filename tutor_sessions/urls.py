from django.urls import path
from . import views

urlpatterns = [ 
    path('session_list/',views.list_session,name='session_list' ),
    path('check_in_out/<int:session_id>/', views.check_in_out, name='check_in_out'),
    path('purchased_packages/',views.list_BaseSession,name='base_session_list' ),
    path('request/<int:pkg_id>/', views.request_session, name='request_session'),   
    path('handle_request/<int:req_id>/', views.handle_request, name='handle_request'),   
    path('requests/', views.session_requests, name='session_requests'),   
    path('reschedule/<int:session_id>/', views.session_reschedule, name='session_reschedule'),   
    path('book/<int:base_id>/',views.book_sessions, name="book_session" ),
    path('cancel/<int:session_id>/',views.cancel_schedule, name="cancel_schedule" ),
    path('payment/verify/<str:tx_ref>/', views.payment_verification, name='verify_payment'),

 
]   
 