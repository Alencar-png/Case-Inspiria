from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    cpf: str
    birth_date: str
    phone: str
    health_insurance: bool
    photo: str

class PatientUpdate(BaseModel):
    name: str
    cpf: str
    birth_date: str
    phone: str
    health_insurance: bool
    photo: str

class PatientResponse(BaseModel):
    id: int
    name: str
    cpf: str
    birth_date: str
    phone: str
    health_insurance: bool
    photo: str

    class Config:
        orm_mode = True