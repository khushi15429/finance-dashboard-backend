from django.contrib import admin
from .models import FinancialRecord


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display  = ('user', 'type', 'category', 'amount', 'date', 'deleted_at')
    list_filter   = ('type', 'category', 'date')
    search_fields = ('user__email', 'notes')
    ordering      = ('-date',)