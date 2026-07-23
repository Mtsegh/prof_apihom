# core/admin.py
from django.contrib import admin

from .models import Profile, SocialLink, Statistic


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'order')
    list_editable = ('value', 'suffix', 'order')
    ordering = ('order',)


