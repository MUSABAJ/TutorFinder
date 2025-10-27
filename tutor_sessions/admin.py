from django.contrib import admin
from .models import BaseSession ,BookedSession,VirtualClass
# Register your models here.  
 
@admin.register(BookedSession)
class BookedSessionAdmin(admin.ModelAdmin):
    list_display = ('base_session', 'schedule_date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'schedule_date')
    search_fields = ('base_session__student__username', 'base_session__tutor_username')

class BookedSessionInline(admin.TabularInline):
    model = BookedSession
    extra = 0

@admin.register(BaseSession)
class BaseSession(admin.ModelAdmin):
    inlines = [BookedSessionInline]
    list_display = ('student', 'tutor', 'total_session','remaining_hours')

@admin.register(VirtualClass)
class VirtualClass(admin.ModelAdmin):
    model  = VirtualClass
    extra = 0
    