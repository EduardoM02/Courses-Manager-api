# CourseManager API

API REST para la gestión completa de cursos en línea. Permite a los instructores crear y administrar cursos, módulos y lecciones, mientras que los estudiantes pueden enrollarse y rastrear su progreso.

## ✨ Características

- 👤 **Autenticación y Autorización** - Sistema JWT con roles (Admin, Instructor, Student)
- 📚 **Gestión de Cursos** - Crear, editar, publicar y eliminar cursos
- 📖 **Módulos y Lecciones** - Organiza el contenido en módulos con lecciones ordenadas
- 📝 **Enrollamiento** - Los estudiantes se pueden inscribir en cursos publicados
- 📊 **Progreso de Lecciones** - Rastreo del progreso de cada estudiante por lección
- 🔒 **Base de Datos PostgreSQL** - Persistencia confiable con SQLAlchemy ORM

## 🚀 Requisitos Previos

- Python 3.10+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd CourseManager
```

### 2. Crear y activar entorno virtual

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `example.env` a `.env` y completa los valores:

```bash
cp app/example.env .env
```

Edita `.env` con tus valores:

```env
PORT=8000
HOST=localhost
DATABASE_URL=postgresql://user:password@localhost:5432/coursemanager
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Crear la base de datos

```bash
createdb coursemanager
```

### 6. Ejecutar las migraciones

```bash
# Si tienes alembic configurado
alembic upgrade head

# O usa el script de inicialización
python -m app.scripts.create_admin
```

## 🏃 Ejecutar la aplicación

```bash
# Desarrollo con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación de API

Una vez que la aplicación está corriendo, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗 Estructura del Proyecto

```
CourseManager/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/        # Rutas por recurso
│   │       │   ├── auth.py
│   │       │   ├── courses.py
│   │       │   ├── enrollment.py
│   │       │   └── users.py
│   │       └── router.py
│   ├── core/
│   │   ├── enums.py              # Enumeraciones (RoleType)
│   │   ├── exceptions.py         # Excepciones personalizadas
│   │   ├── security.py           # Utilidades JWT
│   │   └── exception_handlers.py
│   ├── db/
│   │   ├── session.py            # Configuración de sesión
│   │   └── settings.py           # Variables de entorno
│   ├── models/                   # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── module.py
│   │   ├── lesson.py
│   │   ├── enrollment.py
│   │   └── lesson_progress.py
│   ├── repositories/             # Capa de acceso a datos
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   ├── module_repository.py
│   │   └── enrollment_repository.py
│   ├── schemas/                  # Esquemas Pydantic para validación
│   │   ├── user_schema.py
│   │   ├── course_schema.py
│   │   ├── module_schema.py
│   │   ├── lesson_schema.py
│   │   ├── enrollment_schema.py
│   │   └── lesson_progress_schema.py
│   ├── services/                 # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   └── enrollment_service.py
│   ├── main.py                   # Entrada de la aplicación
│   ├── dependencies.py           # Inyección de dependencias
│   └── example.env
├── .gitignore
└── README.md
```

## 🔐 Autenticación

La API usa **JWT (JSON Web Tokens)** para autenticación:

```bash
# Registrarse
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}

# Iniciar sesión
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

Incluye el token en los headers:

```
Authorization: Bearer <tu_token_jwt>
```

## 📋 Endpoints Principales

### Usuarios
- `POST /api/v1/users` - Crear usuario (Admin)
- `GET /api/v1/users/{user_id}` - Obtener usuario
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario (Admin)

### Cursos
- `POST /api/v1/courses` - Crear curso (Instructor)
- `GET /api/v1/courses` - Listar cursos publicados
- `GET /api/v1/courses/{course_id}` - Obtener detalles del curso
- `PUT /api/v1/courses/{course_id}` - Actualizar curso (Dueño)
- `DELETE /api/v1/courses/{course_id}` - Eliminar curso (Dueño)

### Enrollamiento
- `POST /api/v1/enrollments` - Enrollarse en un curso
- `GET /api/v1/enrollments` - Listar mis enrollamientos
- `DELETE /api/v1/enrollments/{enrollment_id}` - Cancelar inscripción

### Módulos
- `POST /api/v1/modules` - Crear módulo (Instructor)
- `GET /api/v1/modules/{course_id}` - Listar módulos de un curso
- `PUT /api/v1/modules/{module_id}` - Actualizar módulo

### Lecciones
- `POST /api/v1/lessons` - Crear lección
- `GET /api/v1/lessons/{module_id}` - Listar lecciones de un módulo
- `PUT /api/v1/lessons/{lesson_id}` - Actualizar lección

## 🧪 Testing

Usa el archivo `test_main.http` para probar los endpoints con herramientas como REST Client o Postman.

## 👥 Roles y Permisos

| Acción | Admin | Instructor | Student |
|--------|-------|-----------|---------|
| Crear cursos | ✅ | ✅ | ❌ |
| Editar propio curso | ✅ | ✅ | ❌ |
| Eliminar cualquier curso | ✅ | ❌ | ❌ |
| Enrollarse en cursos | ❌ | ❌ | ✅ |
| Ver progreso | ✅ | ✅ | ✅* |

*Los estudiantes solo ven su propio progreso

## 🛠 Desarrollo

### Crear un nuevo endpoint

1. Define el esquema en `schemas/`
2. Crea la ruta en `api/v1/endpoints/`
3. Implementa la lógica en `services/`
4. Usa el repositorio en el servicio

### Ejemplo:

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
    # Lógica aquí
    pass
```

## 📝 Convenciones de Código

- Usa type hints en todas las funciones
- Naming en snake_case para variables y funciones
- Naming en PascalCase para clases
- Docstrings para funciones públicas
- Ancho máximo de línea: 100 caracteres

## 🐛 Solucionar Problemas

### Error: "ModuleNotFoundError"
Asegúrate de que el entorno virtual está activado y las dependencias están instaladas:
```bash
pip install -r requirements.txt
```

### Error: "connection refused" en PostgreSQL
Verifica que PostgreSQL está corriendo y que `DATABASE_URL` es correcto en `.env`.

### Error: "InvalidRequestError" con SQLAlchemy
Asegúrate de que `from __future__ import annotations` está al inicio de los modelos.

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver LICENSE para más detalles.

## 👨‍💻 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Última actualización**: Mayo 2026

