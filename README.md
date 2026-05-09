# CourseManager API

REST API for complete online course management. Allows instructors to create and manage courses, modules, and lessons, while students can enroll and track their progress.

## ✨ Features

- 👤 **Authentication & Authorization** - JWT system with roles (Admin, Instructor, Student)
- 📚 **Course Management** - Create, edit, publish, and delete courses
- 📖 **Modules & Lessons** - Organize content into modules with ordered lessons
- 📝 **Enrollment** - Students can register for published courses
- 📊 **Lesson Progress** - Track each student's progress by lesson
- 🔒 **PostgreSQL Database** - Reliable persistence with SQLAlchemy ORM

## 🚀 Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repository>
cd CourseManager
```

### 2. Create and activate virtual environment

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the `example.env` file to `.env` and complete the values:

```bash
cp app/example.env .env
```

Edit `.env` with your values:

```env
PORT=8000
HOST=localhost
DATABASE_URL=postgresql://user:password@localhost:5432/coursemanager
SECRET_KEY=your-very-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Create the database

```bash
createdb coursemanager
```

### 6. Run migrations

```bash
# If you have alembic configured
alembic upgrade head

# Or use the initialization script
python -m app.scripts.create_admin
```

## 🏃 Running the application

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the application is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗 Project Structure

```
CourseManager/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/        # Routes by resource
│   │       │   ├── auth.py
│   │       │   ├── courses.py
│   │       │   ├── enrollment.py
│   │       │   └── users.py
│   │       └── router.py
│   ├── core/
│   │   ├── enums.py              # Enumerations (RoleType)
│   │   ├── exceptions.py         # Custom exceptions
│   │   ├── security.py           # JWT utilities
│   │   └── exception_handlers.py
│   ├── db/
│   │   ├── session.py            # Session configuration
│   │   └── settings.py           # Environment variables
│   ├── models/                   # SQLAlchemy models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── module.py
│   │   ├── lesson.py
│   │   ├── enrollment.py
│   │   └── lesson_progress.py
│   ├── repositories/             # Data access layer
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   ├── module_repository.py
│   │   └── enrollment_repository.py
│   ├── schemas/                  # Pydantic schemas for validation
│   │   ├── user_schema.py
│   │   ├── course_schema.py
│   │   ├── module_schema.py
│   │   ├── lesson_schema.py
│   │   ├── enrollment_schema.py
│   │   └── lesson_progress_schema.py
│   ├── services/                 # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   └── enrollment_service.py
│   ├── main.py                   # Application entry point
│   ├── dependencies.py           # Dependency injection
│   └── example.env
├── .gitignore
└── README.md
```

## 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication:

```bash
# Register
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}

# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

Include the token in headers:

```
Authorization: Bearer <your_jwt_token>
```

## 📋 Main Endpoints

### Users
- `POST /api/v1/users` - Create user (Admin)
- `GET /api/v1/users/{user_id}` - Get user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user (Admin)

### Courses
- `POST /api/v1/courses` - Create course (Instructor)
- `GET /api/v1/courses` - List published courses
- `GET /api/v1/courses/{course_id}` - Get course details
- `PUT /api/v1/courses/{course_id}` - Update course (Owner)
- `DELETE /api/v1/courses/{course_id}` - Delete course (Owner)

### Enrollment
- `POST /api/v1/enrollments` - Enroll in a course
- `GET /api/v1/enrollments` - List my enrollments
- `DELETE /api/v1/enrollments/{enrollment_id}` - Cancel enrollment

### Modules
- `POST /api/v1/modules` - Create module (Instructor)
- `GET /api/v1/modules/{course_id}` - List course modules
- `PUT /api/v1/modules/{module_id}` - Update module

### Lessons
- `POST /api/v1/lessons` - Create lesson
- `GET /api/v1/lessons/{module_id}` - List module lessons
- `PUT /api/v1/lessons/{lesson_id}` - Update lesson

## 🧪 Testing

Use the `test_main.http` file to test endpoints with tools like REST Client or Postman.

## 👥 Roles & Permissions

| Action | Admin | Instructor | Student |
|--------|-------|-----------|---------|
| Create courses | ✅ | ✅ | ❌ |
| Edit own course | ✅ | ✅ | ❌ |
| Delete any course | ✅ | ❌ | ❌ |
| Enroll in courses | ❌ | ❌ | ✅ |
| View progress | ✅ | ✅ | ✅* |

*Students only see their own progress

## 🛠 Development

### Create a new endpoint

1. Define schema in `schemas/`
2. Create route in `api/v1/endpoints/`
3. Implement logic in `services/`
4. Use repository in the service

### Example:

```python
# schemas/example_schema.py
from pydantic import BaseModel

class ExampleSchema(BaseModel):
    title: str
    description: str

# api/v1/endpoints/example.py
from fastapi import APIRouter
from app.schemas.example_schema import ExampleSchema

router = APIRouter(prefix="/examples", tags=["examples"])

@router.post("/")
async def create_example(schema: ExampleSchema):
    # Logic here
    pass
```

## 📝 Code Conventions

- Use type hints in all functions
- Naming in snake_case for variables and functions
- Naming in PascalCase for classes
- Docstrings for public functions
- Maximum line width: 100 characters

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
Make sure the virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Error: "connection refused" in PostgreSQL
Verify that PostgreSQL is running and `DATABASE_URL` is correct in `.env`.

### Error: "InvalidRequestError" with SQLAlchemy
Make sure `from __future__ import annotations` is at the beginning of models.

## 📄 License

This project is licensed under the MIT License. See LICENSE for details.

## 👨‍💻 Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Last updated**: May 2026

