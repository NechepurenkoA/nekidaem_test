from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="author",
    )
    followers = models.ManyToManyField(
        User, verbose_name="Подписчики", related_name="followers_list"
    )


class Post(models.Model):
    blog = models.ForeignKey(
        Blog, verbose_name="Блоги", related_name="posts", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=140)
    text = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = [
            "created_at",
        ]
