from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from repositories.patient_repository import PatientsRepository
from schemas.patient_schemas import PatientCreate, PatientUpdate, PatientResponse
from typing import List
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

patient = APIRouter()

@patient.post("/patients/", status_code=HTTPStatus.CREATED, response_model=PatientResponse)
def create_patient(patient_data: PatientCreate, repo: PatientsRepository = Depends()):
    return repo.create(patient_data)

@patient.get("/patients/", response_model=List[PatientResponse])
def read_patients(repo: PatientsRepository = Depends()):
    return repo.find_all()

@patient.get("/patients/{patient_id}", response_model=PatientResponse)
def read_patient(patient_id: int, repo: PatientsRepository = Depends()):
    return repo.find_one(patient_id)

@patient.get("/patients/cpf/{cpf}", response_model=PatientResponse)
def read_patient_by_cpf(cpf: str, repo: PatientsRepository = Depends()):
    patient_data = repo.find_by_cpf(cpf)
    if not patient_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Paciente não encontrado.")
    return patient_data

@patient.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient_data: PatientUpdate, repo: PatientsRepository = Depends()):
    return repo.update(patient_id, patient_data)

@patient.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, repo: PatientsRepository = Depends()):
    return repo.delete(patient_id)
