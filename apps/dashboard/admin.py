from django.contrib import admin
from .models import HealthArticle


@admin.register(HealthArticle)
class HealthArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'published_at']
    list_filter = ['is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
