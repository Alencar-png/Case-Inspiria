from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    cpf: str
    birth_date: str
    phone: str
    health_insurance: bool

class PatientUpdate(BaseModel):
    name: str
    cpf: str
    birth_date: str
    phone: str
    health_insurance: bool

class PatientResponse(BaseModel):
    id: int
    name: str
    cpf: str
    birth_date: str
    phone: str
    health_insurance: bool

    class Config:
        orm_mode = True