import pytest


@pytest.fixture
def post(user):
    from blogs.models import Post

    return Post.objects.create(
        title="some text",
        text="some text",
        blog=user.blog,
    )


@pytest.fixture
def post_2(user):
    from blogs.models import Post

    return Post.objects.create(
        title="some text",
        text="some text",
        blog=user.blog,
    )


@pytest.fixture
def post_3(user):
    from blogs.models import Post

    return Post.objects.create(
        title="some text",
        text="some text",
        blog=user.blog,
    )


@pytest.fixture
def post_4(another_user):
    from blogs.models import Post

    return Post.objects.create(
        title="some text",
        text="some text",
        blog=another_user.blog,
    )


@pytest.fixture
def post_5(another_user):
    from blogs.models import Post

    return Post.objects.create(
        title="some text",
        text="some text",
        blog=another_user.blog,
    )


@pytest.fixture
def post_6(another_user):
    from blogs.models import Post

    return Post.objects.create(
        title="some text",
        text="some text",
        blog=another_user.blog,
    )
