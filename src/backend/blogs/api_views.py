from http import HTTPMethod

from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blogs.models import Blog, BlogFollow, Post, PostRead
from blogs.pagination import PageNumberPaginationForPosts
from blogs.permissions import IsAuthenticatedOrAdminForUsers
from blogs.serializers import (
    BlogSerializer,
    FollowBlogSerializer,
    PostSerializer,
    SendToReadSerializer,
)
from blogs.services import BlogFollowService, PostReadService


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticatedOrAdminForUsers,)
    serializer_class = PostSerializer
    pagination_class = PageNumberPaginationForPosts

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=[HTTPMethod.POST],
        detail=True,
    )
    def send_to_read(self, request, pk):
        serializer = SendToReadSerializer(
            data={"post_id": pk}, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        PostReadService(request).send_to_read(post_id=pk)
        added_to_read_blog = PostSerializer(
            get_object_or_404(Post, pk=pk), context=self.get_serializer_context()
        )
        return Response(
            added_to_read_blog.data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        queryset = Post.objects.filter(
            blog_id__in=BlogFollow.objects.filter(
                user_id=self.request.user.id,
            ).values_list("blog_id", flat=True),
        )
        read_flags = PostRead.objects.filter(
            user_id=self.request.user.id,
            flag=True,
        ).values_list("id", flat=True)
        return queryset.exclude(is_read__in=read_flags)


class BlogViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = BlogSerializer

    @action(
        methods=[HTTPMethod.POST],
        detail=True,
        url_path="follow",
    )
    def follow_blog(self, request, pk):
        serializer = FollowBlogSerializer(
            data={"blog_id": pk}, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        BlogFollowService(request).add_follower(pk)
        followed_blog_serialized = BlogSerializer(
            get_object_or_404(Blog, pk=pk), context=self.get_serializer_context()
        )
        return Response(
            followed_blog_serialized.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=[HTTPMethod.DELETE],
        detail=True,
        url_path="unfollow",
    )
    def unfollow_blog(self, request, pk):
        serializer = FollowBlogSerializer(
            data={"blog_id": pk}, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        BlogFollowService(request).remove_follower(pk)
        followed_blog_serialized = BlogSerializer(
            get_object_or_404(Blog, pk=pk), context=self.get_serializer_context()
        )
        return Response(
            followed_blog_serialized.data,
            status=status.HTTP_204_NO_CONTENT,
        )
