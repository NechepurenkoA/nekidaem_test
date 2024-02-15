from django.db import models

from users.models import User


class Blog(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="blog",
    )
    followers = models.ManyToManyField(
        User,
        verbose_name="Подписчики",
        related_name="following_list",
        through="BlogFollow",
    )

    def __str__(self):
        return f"Блог пользователя {self.user.username}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class BlogFollow(models.Model):
    user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name="following", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} подписан на {self.blog.user.username}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписчики"


class Post(models.Model):
    blog = models.ForeignKey(
        Blog, verbose_name="Блоги", related_name="posts", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=140)
    text = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.ManyToManyField(User, through="PostRead", related_name="is_read")

    def __str__(self):
        return f"Пост номер {self.id}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = [
            "created_at",
        ]


class PostRead(models.Model):
    """Пометка прочитанным."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} пометил {self.post.id}"

    class Meta:
        verbose_name = "Помечен как прочтен"
        verbose_name_plural = "Помечены как прочтенные"
