from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'year', 'publication_type')
    list_filter = ('publication_type', 'year')
    search_fields = ('title', 'authors', 'journal', 'doi')
    ordering = ('-year',)
    readonly_fields = ('created_at', 'updated_at')


