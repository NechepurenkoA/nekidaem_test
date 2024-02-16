from http import HTTPStatus


class TestAuthAPI:

    def test_auth(self, client, user, password):
        response = client.post(
            "/api/v1/obtain-token/",
            data={"username": user.username, "password": password},
        )
        assert response.status_code == HTTPStatus.OK, (
            "POST-запрос к `/api/v1/obtain-token/` "
            f"должен возвращать ответ с кодом {HTTPStatus.OK}."
        )

        auth_data = response.json()
        assert "token" in auth_data, "Ответ с корректными данными не содержит токен."

    def test_auth_with_invalid_data(self, client, user):
        response = client.post("/api/v1/obtain-token/", data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Некорректные данные должны "
            f"возвращать ответ статуса {HTTPStatus.BAD_REQUEST}"
        )

    def test_has_blog(self, user):
        assert user.id == user.blog.id, "После создания пользователя не создается блог."
