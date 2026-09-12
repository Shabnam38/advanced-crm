from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'customer', 'value', 'stage', 'probability', 'expected_close_date')
    search_fields = ('title',)
    list_filter = ('stage',)
    ordering = ('-created_at',)