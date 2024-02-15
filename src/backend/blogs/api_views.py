from rest_framework import mixins, viewsets

from blogs.models import BlogFollow, Post, PostRead
from blogs.pagination import PageNumberPaginationForPosts
from blogs.permissions import IsAuthenticatedOrAdminForUsers
from blogs.serializers import PostSerializer


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticatedOrAdminForUsers,)
    serializer_class = PostSerializer
    pagination_class = PageNumberPaginationForPosts

    def get_queryset(self):
        queryset = Post.objects.filter(
            blog_id__in=BlogFollow.objects.filter(
                user_id=self.request.user.id,
            ).values_list("blog_id", flat=True),
        )
        read_flags = PostRead.objects.filter(
            user_id=self.request.user.id,
        ).values_list("id", flat=True)
        return queryset.exclude(is_read__in=read_flags)
