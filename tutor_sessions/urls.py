from django.urls import path
from . import views

urlpatterns = [ 
    path('session_list/',views.list_session,name='session_list' ),
    path('purchased_packages/',views.list_BaseSession,name='base_session_list' ),
    path('details/<str:bs_id>',views.base_session_detail,name='base_session_detail'),
    path('session_packages',views.base_session_manager, name='base_session_manage'),
    path('requests/', views.session_requests, name='session_requests'),   
    path('request/<int:pkg_id>/', views.request_session, name='request_session'),   
    # path('handle_request/<int:req_id>/', views.handle_request, name='handle_request'),   
    path('reschedule/<int:session_id>/', views.session_reschedule, name='session_reschedule'),   
    path('book/<int:base_id>/',views.book_sessions, name="book_session" ),
    path('cancel/<int:session_id>/',views.cancel_schedule, name="cancel_schedule" ),
    path('payment/verify/<str:tx_ref>/', views.payment_verification, name='verify_payment'),

 
]   
 