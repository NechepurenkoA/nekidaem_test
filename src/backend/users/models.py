from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name="Эл. почта", unique=True, null=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "username",
        ]


# Вынужденная мера, т.к. User используется в блоге как FK
from blogs.models import Blog  # noqa


def create_blog(sender, instance, created, **kwargs):
    """Создание блога при создании пользователя."""
    if created:
        Blog.objects.create(user=instance)


models.signals.post_save.connect(
    create_blog, sender=User, weak=False, dispatch_uid="models.create_blog"
)
