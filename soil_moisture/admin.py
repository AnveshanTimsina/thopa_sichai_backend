from django.contrib import admin
from .models import SoilMoisture


@admin.register(SoilMoisture)
class SoilMoistureAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'ip_address']
    search_fields = ['ip_address', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

