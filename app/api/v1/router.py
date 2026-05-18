from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, courses, enrollment, module, lesson


api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(courses.router, tags=["courses"])
api_router.include_router(enrollment.router, tags=["enrollment"])
api_router.include_router(module.router, tags=["modules"])
api_router.include_router(lesson.router, tags=["lesson"])