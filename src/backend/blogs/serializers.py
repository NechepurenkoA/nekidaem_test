from http import HTTPMethod

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.validators import ValidationError

from blogs.models import Blog, BlogFollow, Post, PostRead


class BlogSerializer(serializers.ModelSerializer):
    """Сериализатор модели 'Blog'."""

    is_followed = serializers.SerializerMethodField(method_name="get_is_followed")

    def get_is_followed(self, blog_id):
        return BlogFollow.objects.filter(
            user_id=self.context["request"].user.id,
            blog_id=blog_id,
        ).exists()

    class Meta:
        model = Blog
        fields = [
            "id",
            "is_followed",
            "followers",
        ]


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели 'Post'."""

    is_read = serializers.SerializerMethodField(
        method_name="get_is_read",
    )

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "blog": {
                "read_only": True,
            },
            "text": {
                "required": False,
            },
        }

    def get_is_read(self, post_id):
        return PostRead.objects.filter(
            post_id=post_id, user_id=self.context["request"].user.id
        ).exists()

    def create(self, validated_data):
        instance = Post.objects.create(
            **validated_data, blog_id=self.context["request"].user.id
        )
        return instance


class SendToReadSerializer(serializers.Serializer):

    post_id = serializers.IntegerField()

    def validate(self, data):
        request = self.context["request"]
        if PostRead.objects.filter(
            user_id=request.user.id, post_id=data["post_id"]
        ).exists():
            raise ValidationError({"error": "Вы уже добавили этот пост в прочитанные!"})
        return data


class FollowBlogSerializer(serializers.Serializer):
    """Сериализатор подписок на блоги других пользователей."""

    blog_id = serializers.IntegerField()

    def validate(self, data):
        request: Request = self.context["request"]
        if request.user.id == data["blog_id"]:
            raise ValidationError(
                {"error": "Нельзя проводить подобные операции с собой!"}
            )
        if request.method == HTTPMethod.POST:
            if BlogFollow.objects.filter(
                user_id=request.user.id, blog_id=data["blog_id"]
            ).exists():
                raise ValidationError(
                    {"error": "Вы уже подписаны на этого пользователя!"}
                )
        if request.method == HTTPMethod.DELETE:
            if not BlogFollow.objects.filter(
                user_id=request.user.id, blog_id=data["blog_id"]
            ).exists():
                raise ValidationError(
                    {"error": "Вы не подписаны на этого пользователя!"}
                )
        return data
