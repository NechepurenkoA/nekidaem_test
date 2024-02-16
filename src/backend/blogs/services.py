from rest_framework.request import Request

from blogs.models import BlogFollow, PostRead


class PostReadService(object):

    def __init__(self, request: Request):
        self.request = request

    def send_to_read(self, post_id: int) -> None:
        PostRead.objects.create(
            user_id=self.request.user.id,
            post_id=post_id,
            flag=True,
        )
        return None


class BlogFollowService(object):

    def __init__(self, request: Request):
        self.request = request

    def add_follower(self, blog_id: int) -> None:
        BlogFollow.objects.create(
            user_id=self.request.user.id,
            blog_id=blog_id,
        )
        return None

    def remove_follower(self, blog_id: int) -> None:
        BlogFollow.objects.filter(
            user_id=self.request.user.id,
            blog_id=blog_id,
        ).delete()
        return None
