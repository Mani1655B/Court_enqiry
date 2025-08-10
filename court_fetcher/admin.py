from django.contrib import admin
from .models import QueryLog

# Register your models here.
@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('case_type', 'case_number', 'filing_year', 'query_time')
