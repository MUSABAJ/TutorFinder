from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['session', 'status', 'amount', 'updated_at']
    list_filter = ['status']
    readonly_fields = ['updated_at']