from rest_framework.pagination import PageNumberPagination

from blogs.constants import DEFAULT_PAGINATION_PAGE_SIZE, MAX_PAGINATION_PAGE_SIZE


class PageNumberPaginationForPosts(PageNumberPagination):
    """Пагинатор для пагинации постов."""

    page_size = DEFAULT_PAGINATION_PAGE_SIZE
    max_page_size = MAX_PAGINATION_PAGE_SIZE
