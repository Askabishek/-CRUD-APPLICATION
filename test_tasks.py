import pytest


def test_create_task(client, auth_headers):
    response = client.post(
        "/tasks/",
        json={"title": "Buy groceries", "description": "Milk, eggs, bread"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False


def test_create_task_unauthenticated(client):
    response = client.post("/tasks/", json={"title": "Secret task"})
    assert response.status_code == 403


def test_get_tasks(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers)

    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


def test_get_tasks_filter_completed(client, auth_headers):
    resp1 = client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    task_id = resp1.json()["id"]
    client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers)

    # Mark task 1 as completed
    client.put(f"/tasks/{task_id}", json={"completed": True}, headers=auth_headers)

    response = client.get("/tasks/?completed=true", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_get_task_by_id(client, auth_headers):
    create_resp = client.post("/tasks/", json={"title": "My Task"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "My Task"


def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    create_resp = client.post("/tasks/", json={"title": "Old Title"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New Title", "completed": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["completed"] is True


def test_delete_task(client, auth_headers):
    create_resp = client.post("/tasks/", json={"title": "To Delete"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_user_cannot_access_another_users_task(client):
    # Register two users
    client.post(
        "/auth/register",
        json={"username": "user1", "email": "user1@test.com", "password": "pass1"},
    )
    client.post(
        "/auth/register",
        json={"username": "user2", "email": "user2@test.com", "password": "pass2"},
    )

    token1 = client.post("/auth/login", json={"username": "user1", "password": "pass1"}).json()["access_token"]
    token2 = client.post("/auth/login", json={"username": "user2", "password": "pass2"}).json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User1 creates a task
    task_resp = client.post("/tasks/", json={"title": "User1 Task"}, headers=headers1)
    task_id = task_resp.json()["id"]

    # User2 tries to access it — should get 404
    response = client.get(f"/tasks/{task_id}", headers=headers2)
    assert response.status_code == 404


def test_pagination(client, auth_headers):
    for i in range(15):
        client.post("/tasks/", json={"title": f"Task {i}"}, headers=auth_headers)

    response = client.get("/tasks/?page=1&page_size=10", headers=auth_headers)
    data = response.json()
    assert data["total"] == 15
    assert len(data["tasks"]) == 10
    assert data["total_pages"] == 2
