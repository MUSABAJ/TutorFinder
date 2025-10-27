from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'title','file', 'uploaded_at')
    list_filter = ('subject',)
    search_fields = ('tutor__username',)