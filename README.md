# ToDo REST API

A simple and efficient ToDo REST API built with FastAPI, SQLAlchemy, and SQLite.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete tasks
- **Data Validation**: Pydantic models for request/response validation
- **Database**: SQLite with SQLAlchemy ORM
- **Auto-generated Documentation**: Interactive API docs via FastAPI
- **Tested**: Comprehensive test suite with pytest
- **CI/CD**: GitHub Actions for linting and testing

## Requirements

- Python 3.11+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/213yuka/coding-agent-test.git
cd coding-agent-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Create a Task
```http
POST /tasks
```

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "todo",
  "due_date": "2024-12-31"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "todo",
  "due_date": "2024-12-31"
}
```

### List All Tasks
```http
GET /tasks
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "todo",
    "due_date": "2024-12-31"
  }
]
```

### Get a Specific Task
```http
GET /tasks/{task_id}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "todo",
  "due_date": "2024-12-31"
}
```

### Update a Task
```http
PUT /tasks/{task_id}
```

**Request Body:**
```json
{
  "status": "done"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "done",
  "due_date": "2024-12-31"
}
```

### Delete a Task
```http
DELETE /tasks/{task_id}
```

**Response:** `204 No Content`

## Task Model

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | integer | auto | - | Unique identifier |
| title | string | yes | - | Task title |
| description | string | no | null | Task description |
| status | enum | no | "todo" | Task status (todo, done) |
| due_date | date | no | null | Due date (YYYY-MM-DD) |

## Running Tests

Run the test suite:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Linting

Check code quality with ruff:
```bash
ruff check .
```

## CI/CD

The project includes GitHub Actions workflows for:
- **Linting**: Automatically runs ruff on all code
- **Testing**: Runs the full test suite

Workflows are triggered on:
- Push to `main` branch
- Pull requests to `main` branch

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic validation models
│   └── database.py      # Database configuration
├── tests/
│   ├── __init__.py
│   └── test_api.py      # API endpoint tests
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI workflow
├── requirements.txt     # Project dependencies
├── .gitignore
└── README.md
```

## License

MIT