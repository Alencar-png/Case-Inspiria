from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from repositories.doctor_repository import DoctorsRepository
from schemas.doctor_schemas import DoctorCreate, DoctorUpdate, DoctorResponse
from typing import List
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

doctor = APIRouter()

@doctor.post("/doctors/", status_code=HTTPStatus.CREATED, response_model=DoctorResponse)
def create_doctor(doctor_data: DoctorCreate, repo: DoctorsRepository = Depends()):
    return repo.create(doctor_data)

@doctor.get("/doctors/", response_model=List[DoctorResponse])
def read_doctors(repo: DoctorsRepository = Depends()):
    return repo.find_all()

@doctor.get("/doctors/{doctor_id}", response_model=DoctorResponse)
def read_doctor(doctor_id: int, repo: DoctorsRepository = Depends()):
    return repo.find_one(doctor_id)

@doctor.put("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_data: DoctorUpdate, repo: DoctorsRepository = Depends()):
    return repo.update(doctor_id, doctor_data)

@doctor.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, repo: DoctorsRepository = Depends()):
    return repo.delete(doctor_id)

@doctor.get("/doctors/specialty/{specialty}", response_model=List[DoctorResponse])
def read_doctors_by_specialty(specialty: str, repo: DoctorsRepository = Depends()):
    return repo.find_by_specialty(specialty)