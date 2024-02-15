from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationForPosts(LimitOffsetPagination):
    default_limit = 500
