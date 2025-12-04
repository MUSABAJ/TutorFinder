from django.urls import path, include
from . import views
urlpatterns = [
     path('',views.index, name='index'),
     path('student/dashboard',views.student_dashbord, name='student_dashboard'),
     path('tutor/dashboard',views.tutor_dashbord, name='tutor_dashbord'),
     path('tutor/students',views.my_students, name='my_students'),
    path('tutor/packages',views.manage_package,name='manage_package'),
     path('tutor/earning',views.earning,name='earning'),
    path('tutor/view_student/<str:student_id>',views.view_student,name='view_student'),

    path('student/tutors',views.my_tutors,name='my_tutors'), 
    path('student/view_tutor/<str:tutor_id>',views.view_tutor,name='view_tutor'),
     path('student/payment_history',views.payment_history,name='payment_history'),

    path('search/', views.main_serach, name="main_search"),
    path('search/tutor/', views.tutor_serach, name="tutor_search"),
    path('my_profile/',views.my_profile,name='my_profile'),
    path('search/my_tutor/', views.my_tutor_search, name="my_tutor_search")

]
