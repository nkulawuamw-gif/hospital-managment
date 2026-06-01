from django.db import models
from django.utils.text import slugify


class HealthArticle(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True, help_text="Short summary shown on the landing page")
    icon = models.CharField(max_length=50, default="bi bi-heart-pulse-fill", help_text="Bootstrap icon class")
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'health_articles'
        ordering = ['-published_at']
        verbose_name = 'Health Article'
        verbose_name_plural = 'Health Articles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
