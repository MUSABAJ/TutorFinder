from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from .models import TutorProfile
from notifications.utils import create_notification
from django.contrib import messages

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
    list_display = ('user', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'subjects')

    actions = ['verify_selected_tutors', 'unverify_selected_tutors']

    @admin.action(description='Verify selected tutors')
    def verify_selected_tutors(self, request, queryset):
        users_to_notify = [tutor.user for tutor in queryset]
        
        updated_count = queryset.update(is_verified=True)
        
        for user in users_to_notify:
            create_notification(
                recipient=user,
                user=request.user,
                type='important_announcement',
                link="#")
        
        self.message_user(request, f"Successfully verified {updated_count} tutor(s).")

    @admin.action(description='Unverify selected tutors')
    def unverify_selected_tutors(self, request, queryset):

        users_to_notify = [tutor.user for tutor in queryset]
        
        updated_count = queryset.update(is_verified=False)
        
        for user in users_to_notify:
            create_notification(
                recipient=user,
                user=request.user,
                type='important_announcement', 
                link="#")
 
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
    