from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'status', 'score', 'source', 'company_name', 'created_at')
    search_fields = ('full_name', 'email', 'company_name')
    list_filter = ('status', 'source')