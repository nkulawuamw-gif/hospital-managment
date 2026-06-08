from django.contrib import admin
from .models import (
    HealthArticle, ServiceCategory, ServiceItem, Department,
    Testimonial, Statistic, ContactInfo, WhyChooseItem,
    SiteSetting, HeroSection,
)


class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    inlines = [ServiceItemInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'opening_hours', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': ('name', 'icon', 'description', 'order', 'is_active')
        }),
        ('Operating Hours', {
            'fields': ('opening_hours',)
        }),
        ('Client Handling Workflow', {
            'fields': ('client_handling_steps',)
        }),
        ('Referral Network', {
            'fields': ('referrals_from', 'referrals_to'),
            'description': 'Entry / exit points. List department names that refer patients in (from) and out (to).'
        }),
        ('Team Composition', {
            'fields': ('roles',)
        }),
        ('Treatments & Support', {
            'fields': ('treatments',),
            'description': 'List the treatments and patient-support services offered by this department.'
        }),
    )


@admin.register(WhyChooseItem)
class WhyChooseItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'designation', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['patient_name', 'content']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'value']
    search_fields = ['label']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['label', 'info_type', 'value', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['info_type']
    search_fields = ['label', 'value']


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name']


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['headline', 'is_active']


@admin.register(HealthArticle)
class HealthArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'published_at']
    list_filter = ['is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
