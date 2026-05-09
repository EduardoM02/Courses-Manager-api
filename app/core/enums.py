from enum import Enum

class RoleType(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"