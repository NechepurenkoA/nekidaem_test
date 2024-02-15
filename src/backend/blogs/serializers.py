from rest_framework import serializers

from blogs.models import Blog, Post, PostRead


class BlogSerialzier(serializers.ModelSerializer):
    """Сериализатор модели 'Blog'."""

    class Meta:
        model = Blog
        fields = "__all__"


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


class FollowBlogSerializer(serializers.Serializer):
    """Сериализатор подписок на блоги других пользователей."""

    ...
