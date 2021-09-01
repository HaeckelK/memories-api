from app.app import create_app


def test_index() -> None:
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Memories API" in response.data


def test_memories_get() -> None:
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/memories")
        assert response.status_code == 200


def test_memories_get_id_not_found() -> None:
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/memories/999")
        assert response.status_code == 400
