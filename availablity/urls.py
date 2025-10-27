from django.urls import path
from . import views

urlpatterns = [
    path('create_package/',views.create_package,name='create_package'),
    path('list_packages/<int:tutor_id>/',views.package_list,name='list_packages'),
    path('set/', views.set_availablity, name='set_availablity'), 
    path('delete_package/<int:pkg_id>/', views.delete_pkg, name='delete_pkg'), 
    path('togle_package/<int:pkg_id>/', views.togle_pkg, name='togle_pkg'), 
]
