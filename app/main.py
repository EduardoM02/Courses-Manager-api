from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.enums import RoleType
from app.models import (
    User,
    Course,
    Module,
    Lesson,
    LessonProgress,
    Enrollment,
)
from app.core.exceptions import (
    NotFoundError,
    ForbiddenError,
    BadRequestError
)

from app.core.exception_handlers import (
    not_found_handler,
    forbidden_handler,
    bad_request_handler
)

app = FastAPI()

app.include_router(api_router)
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(ForbiddenError, forbidden_handler)
app.add_exception_handler(BadRequestError, bad_request_handler)

@app.get("/")
async def root():
    return {"message": "Hello World"}
