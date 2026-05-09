from datetime import datetime
from pydantic import BaseModel, ConfigDict

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

class EnrollmentRequest(BaseModel):
    module_id: int
    course_id: int

    model_config = ConfigDict(from_attributes=True)
