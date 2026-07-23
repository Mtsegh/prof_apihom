from django.contrib import admin

from .models import (
    ResearchInterest, ResearchProject, Collaborator, Grant, Dataset,
    TeachingResource,
)


@admin.register(ResearchInterest)
class ResearchInterestAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'funding_source')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('name', 'affiliation')
    search_fields = ('name', 'affiliation')
    ordering = ('name',)


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ('title', 'funding_body', 'amount', 'year')
    list_filter = ('year',)
    search_fields = ('title', 'funding_body')
    ordering = ('-year',)


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    ordering = ('-published_date',)
    search_fields = ('title', 'description')


@admin.register(TeachingResource)
class TeachingResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'semester', 'order')
    list_editable = ('order',)
    list_filter = ('course', 'semester')
    search_fields = ('title', 'course', 'description')
    ordering = ('course', 'order')


