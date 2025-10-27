from django.urls import path, include
from . import views
urlpatterns = [
     path('',views.index, name='index'),
     path('student/dashboard',views.student_dashbord, name='student_dashbord'),
     path('tutor/dashboard',views.tutor_dashbord, name='tutor_dashbord'),
     path('tutor/session',views.manage_session, name='manage_session'),
     path('tutor/resources',views.manage_resource, name='manage_resource'),
     path('tutor/students',views.my_students, name='my_students'),
    path('tutor/packages',views.manage_package,name='manage_package'),
    path('tutor/notifications',views.notification,name='notification'),
    path('tutor/earning',views.earning,name='earning'),
    path('tutor/tutor_profile',views.tutor_profile,name='tutor_profile'),

    path('student/tutors',views.my_tutors,name='my_tutors'),
    path('student/sessions',views.my_sessions,name='my_sessions'),
    path('student/resources',views.my_resources,name='resources'),
    path('student/chats',views.chats,name='chats'),
    path('student/payments',views.my_sessions,name='payments'),
    path('student/book_session',views.my_sessions,name='book_session'),
    path('student/view_tutor/<str:tutor_id>',views.view_tutor,name='view_tutor'),
]
