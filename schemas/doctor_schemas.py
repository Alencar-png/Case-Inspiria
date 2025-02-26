from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    specialty: str
    crm: str

class DoctorUpdate(BaseModel):
    name: str
    specialty: str
    crm: str

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialty: str
    crm: str

    class Config:
        orm_mode = True