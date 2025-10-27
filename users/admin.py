from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(User) 
class UsereAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','username','gender','role','email','phone')
    list_filter = ('role','gender','date_of_birth')
    search_fields = ('username', 'email')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user__gender',)
    search_fields = ('user__username', 'user__email')


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified' )
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'user__email')
    
 
#custome Admin Table to minimize unnecesary attribuits

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info',{
            'fields': ('role', 'phone','bio', 
                        'profile_picture', 'location',
                            'date_of_birth' ,'gender')
        }            
        )
    )