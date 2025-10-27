from django.contrib import admin
from .models import TutorPackage, Availablity


@admin.register(TutorPackage)
class TutorPackageAdmin(admin.ModelAdmin):
    list_display = ('tutor','name','total_session', 'session_type','price')
    list_filter = ('is_active',)
@admin.register(Availablity)
class AvailablityAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'updated_at')
    list_filter = ('updated_at',)
    

 