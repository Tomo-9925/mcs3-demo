from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import News, Work

class NewsAdmin(MarkdownxModelAdmin):
  list_display = ('title', 'is_draft', 'published_at', 'updated_at')

class WorkAdmin(admin.ModelAdmin):
  list_display = ('title', 'video_id', 'published_at', 'updated_at')

admin.site.register(News, NewsAdmin)
admin.site.register(Work, WorkAdmin)
