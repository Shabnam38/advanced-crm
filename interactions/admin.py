from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('interaction_type', 'lead', 'customer', 'date')
    list_filter = ('interaction_type',)