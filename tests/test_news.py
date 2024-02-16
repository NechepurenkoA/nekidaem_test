from http import HTTPStatus

import pytest

from blogs.models import Post


class TestNewsAPI:

    @pytest.mark.django_db(transaction=True)
    def test_post_auth_create(self, client, user_client):
        posts_count = Post.objects.count()

        data = {"blog": user_client.id, "title": "some title", "text": "some text"}
        response = client.post("/api/v1/news/", data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            f"Возвращается некорректный код при создании поста. "
            f"Нужен: {HTTPStatus.CREATED}"
        )

        assert posts_count != Post.objects.count(), "Пост не создался."

    @pytest.mark.django_db(transaction=True)
    def test_post_not_auth_create(self, client, another_user):
        posts_count = Post.objects.count()

        data = {"blog": another_user.id, "title": "some title", "text": "some text"}
        response = client.post("/api/v1/news/", data=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f"Возвращается некорректный код при создании поста. "
            f"Нужен: {HTTPStatus.UNAUTHORIZED}"
        )

        assert (
            posts_count == Post.objects.count()
        ), "Пост не должен создаваться когда обращается неавторизованный пользователь."

    @pytest.mark.django_db(transaction=True)
    def test_post_auth_delete(self, user_client, post_3):
        posts_count = Post.objects.count()
        response = user_client.delete(f"/api/v1/news/{post_3.id}/")
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f"Возвращается некорректный код при создании поста. "
            f"Нужен: {HTTPStatus.NO_CONTENT}"
        )

        assert (
            posts_count != Post.objects.count()
        ), "Пост авторизованного пользователя не удаляется."

    def test_news_get(self, client, user_client):
        response = user_client.get("/api/v1/news/")

        assert response.status_code == HTTPStatus.OK, (
            f"При авторизованном запросе на просмотр новостей. "
            f"возвращается не тот код. Ожидается: {HTTPStatus.OK}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_follow(self, user_client, another_user):
        response = user_client.post(f"/api/v1/blogs/{another_user.blog.id}/follow/")
        assert response.status_code == HTTPStatus.CREATED, (
            f"Возвращается некорректный код при подписке на пользователя. "
            f"Нужен: {HTTPStatus.CREATED}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_unfollow(self, user_client, another_user):
        user_client.post(f"/api/v1/blogs/{another_user.blog.id}/follow/")
        followers_count = another_user.blog.followers.count()
        response = user_client.delete(f"/api/v1/blogs/{another_user.blog.id}/unfollow/")
        followers_count_after_deletion = another_user.blog.followers.count()
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f"Возвращается некорректный код при подписке на пользователя. "
            f"Нужен: {HTTPStatus.NO_CONTENT}"
        )
        assert (
            followers_count != followers_count_after_deletion
        ), "Авторизованный подписанный пользователь не отписывается."

    @pytest.mark.django_db(transaction=True)
    def test_correct_news(self, user_client, post_4, post_5, post_6, another_user):
        user_client.post(f"/api/v1/blogs/{another_user.id}/follow/")
        response = user_client.get("/api/v1/news/")
        user_posts_count = another_user.blog.posts.all().count()
        news_posts_count = response.json()["count"]
        assert (
            user_posts_count == news_posts_count
        ), "Новостная лента возвращает некорректный ответ."

    def test_correct_after_to_read_news(
        self, user_client, post_4, post_5, post_6, another_user
    ):
        user_client.post(f"/api/v1/blogs/{another_user.id}/follow/")
        response = user_client.get("/api/v1/news/")
        posts_count = response.json()["count"]
        user_client.post(f"/api/v1/news/{post_6.id}/send_to_read/")
        response_2 = user_client.get("/api/v1/news/")
        posts_count_2 = response_2.json()["count"]
        assert posts_count != posts_count_2, "Пост не удалился из новостной ленты."
