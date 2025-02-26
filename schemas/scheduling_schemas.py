from pydantic import BaseModel
from enum import Enum
from typing import Optional
from uuid import UUID

class SchedulingType(str, Enum):
    CONSULTATION = "CONSULTATION"
    RETURN = "RETURN"
    EXAM = "EXAM"

class SchedulingCreate(BaseModel):
    scheduling_date: str
    scheduling_time: str
    scheduling_type: SchedulingType
    doctor_id: int
    patient_id: int
    rescheduled: Optional[bool] = False

class SchedulingUpdate(BaseModel):
    scheduling_date: str
    scheduling_time: str
    scheduling_type: SchedulingType
    doctor_id: int
    patient_id: int
    rescheduled: Optional[bool] = False

class SchedulingResponse(BaseModel):
    id: UUID
    scheduling_date: str
    scheduling_time: str
    scheduling_type: SchedulingType
    doctor_id: int
    patient_id: int
    rescheduled: bool

    class Config:
        orm_mode = True
