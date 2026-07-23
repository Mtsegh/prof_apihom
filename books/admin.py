from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'price', 'currency', 'availability', 'featured_order',
    )
    list_editable = ('category', 'price', 'currency', 'availability', 'featured_order')
    list_filter = ('availability', 'currency', 'category')
    search_fields = ('title', 'subtitle', 'isbn', 'publisher')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')


