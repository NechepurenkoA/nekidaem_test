from django.contrib import admin

from blogs.models import Blog, BlogFollow, PostRead


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"


@admin.register(BlogFollow)
class BlogFollow(admin.ModelAdmin):
    empty_value_display = "-пусто-"


@admin.register(PostRead)
class PostRead(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
    )
    search_fields = ("flag",)
    empty_value_display = "-пусто-"
