from django.contrib import admin
from .models import FeedBack


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'feedback', 'rating','created_at')
    list_filter = ('rating','created_at')
