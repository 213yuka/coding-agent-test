import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_task():
    """Test creating a new task"""
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "todo"
    assert "id" in data


def test_create_task_with_all_fields():
    """Test creating a task with all fields"""
    response = client.post(
        "/tasks",
        json={
            "title": "Complete Task",
            "description": "Full description",
            "status": "done",
            "due_date": "2024-12-31"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Complete Task"
    assert data["status"] == "done"
    assert data["due_date"] == "2024-12-31"


def test_create_task_without_title():
    """Test that creating a task without title fails"""
    response = client.post(
        "/tasks",
        json={"description": "No title"}
    )
    assert response.status_code == 422


def test_create_task_with_empty_title():
    """Test that creating a task with empty title fails"""
    response = client.post(
        "/tasks",
        json={"title": ""}
    )
    assert response.status_code == 422


def test_create_task_with_invalid_status():
    """Test that creating a task with invalid status fails"""
    response = client.post(
        "/tasks",
        json={"title": "Test", "status": "invalid"}
    )
    assert response.status_code == 422


def test_list_tasks():
    """Test listing all tasks"""
    # Create some tasks
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_list_tasks_empty():
    """Test listing tasks when none exist"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_task():
    """Test getting a specific task"""
    create_response = client.post(
        "/tasks",
        json={"title": "Test Task"}
    )
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_get_task_not_found():
    """Test getting a non-existent task"""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    """Test updating a task"""
    create_response = client.post(
        "/tasks",
        json={"title": "Original Title", "status": "todo"}
    )
    task_id = create_response.json()["id"]
    
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Title", "status": "done"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "done"


def test_update_task_partial():
    """Test partially updating a task"""
    create_response = client.post(
        "/tasks",
        json={"title": "Original Title", "description": "Original"}
    )
    task_id = create_response.json()["id"]
    
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"status": "done"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Original Title"
    assert data["status"] == "done"


def test_update_task_not_found():
    """Test updating a non-existent task"""
    response = client.put(
        "/tasks/999",
        json={"title": "Updated"}
    )
    assert response.status_code == 404


def test_delete_task():
    """Test deleting a task"""
    create_response = client.post(
        "/tasks",
        json={"title": "Task to Delete"}
    )
    task_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting a non-existent task"""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
