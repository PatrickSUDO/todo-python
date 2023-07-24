from unittest.mock import patch
from fastapi.testclient import TestClient
from unittest.mock import Mock
from src.main import app
from src.schemas.todos import Todo as TodoSchema
from src.db.models import Todo as TodoModel

client = TestClient(app)


def test_read_todos():
    with patch("src.db.database.database.fetch_all") as mock_fetch_all:
        test_todo = TodoSchema(
            id=1, task="test_read_todos", completed=False, deleted=False
        )

        mock_fetch_all.return_value = [test_todo]

        response = client.get("/v1/todos/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["task"] == "test_read_todos"
        assert not response.json()[0]["completed"]
        assert not response.json()[0]["deleted"]

        mock_fetch_all.assert_called_once()


def test_create_todo():
    with patch("src.db.database.database.fetch_one") as mock_fetch_one:
        test_todo = TodoSchema(
            id=1, task="test_create_todo", completed=False, deleted=False
        )
        mock_fetch_one.return_value = test_todo.model_dump()

        response = client.post("/v1/todos/", json=test_todo.model_dump())

        assert response.status_code == 201
        assert response.json() == test_todo.model_dump()
        mock_fetch_one.assert_called_once()


def test_read_todo():
    with patch("src.db.database.database.fetch_one") as mock_fetch_one:
        test_todo = TodoSchema(
            id=1, task="test_read_todo", completed=False, deleted=False
        )
        mock_fetch_one.return_value = test_todo

        response = client.get("/v1/todos/1")

        assert response.status_code == 200
        assert response.json() == test_todo.model_dump()

        mock_fetch_one.assert_called_once()


def test_update_todo():
    with patch("src.db.database.database.fetch_one") as mock_fetch_one:
        original_todo = TodoSchema(
            id=1, task="Original task", completed=False, deleted=False
        )
        updated_todo = TodoSchema(
            id=1, task="Updated task", completed=True, deleted=False
        )

        mock_fetch_one.return_value = updated_todo.model_dump()

        response = client.put(
            f"/v1/todos/{original_todo.id}", json=updated_todo.model_dump()
        )

        assert response.status_code == 200
        assert response.json()["task"] == "Updated task"
        assert response.json()["completed"]
        assert not response.json()["deleted"]

        mock_fetch_one.assert_called_once()


def test_delete_todo():
    with patch("src.db.database.database.fetch_one") as mock_fetch_one:
        test_todo = TodoSchema(id=1, task="Test task", completed=False, deleted=False)
        mock_fetch_one.return_value = test_todo.model_dump()

        response = client.delete(f"/v1/todos/{test_todo.id}")

        assert response.status_code == 204
        mock_fetch_one.assert_called_once()


def test_read_completed_todos():
    with patch("src.db.database.database.fetch_all") as mock_fetch_all:
        test_todo_1 = TodoSchema(
            id=1, task="test_read_completed_todos", completed=True, deleted=False
        )
        test_todo_2 = TodoSchema(
            id=1, task="test_read_completed_todos", completed=False, deleted=False
        )

        mock_fetch_all.return_value = [test_todo_1, test_todo_2]

        response = client.get("/v1/todos/completed")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["task"] == "test_read_completed_todos"
        assert response.json()[0]["completed"]
        assert not response.json()[0]["deleted"]

        mock_fetch_all.assert_called_once()


def test_read_deleted_todos():
    with patch("src.db.database.database.fetch_all") as mock_fetch_all, \
            patch("src.db.models.Todo.__table__.select") as mock_select:
        test_todo_1 = TodoSchema(id=1, task="not deleted", completed=False, deleted=False)
        test_todo_2 = TodoSchema(id=1, task="deleted todo", completed=False, deleted=True)
        mock_where = Mock()
        mock_where.return_value = TodoModel.__table__

        mock_select.return_value.where = mock_where

        mock_fetch_all.return_value = [test_todo_1, test_todo_2]

        response = client.get("/v1/todos/deleted")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["task"] == "deleted todo"
        assert not response.json()[0]["completed"]
        assert response.json()[0]["deleted"]

        mock_fetch_all.assert_called_once()


def test_update_non_existent_todo():
    with patch("src.db.database.database.fetch_one") as mock_fetch_one:
        mock_fetch_one.return_value = None

        test_todo = TodoSchema(id=1, task="Test task", completed=False, deleted=False)

        response = client.put("/v1/todos/1", json=test_todo.model_dump())

        assert response.status_code == 404

        mock_fetch_one.assert_called_once()
