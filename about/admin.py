from django.contrib import admin
from .models import AboutContent, Education, CareerMilestone, Membership, Skill


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return not AboutContent.objects.exists()


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year', 'order')
    list_editable = ('order',)
    ordering = ('-end_year',)
    search_fields = ('degree', 'institution')


@admin.register(CareerMilestone)
class CareerMilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'start_year', 'end_year')
    ordering = ('start_year',)
    search_fields = ('title', 'organization')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('organization', 'role', 'year_joined')
    ordering = ('year_joined',)
    search_fields = ('organization',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

