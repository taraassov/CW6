from django.contrib import admin

from blogpost.models import Blogpost


@admin.register(Blogpost)
class ClientBlogpost(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'created_at', 'is_published')

