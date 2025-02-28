from fastapi import Depends, HTTPException
from repositories.base_repository import BaseRepository, CRUDBase
from schemas.doctor_schemas import DoctorCreate, DoctorUpdate
from models.models import Doctor
import logging

logger = logging.getLogger(__name__)

class DoctorsRepository(CRUDBase):
    def __init__(self, base_repository: BaseRepository = Depends()):
        self.base_repository = base_repository

    @property
    def _entity(self):
        return Doctor

    def crm_exists(self, crm: str, doctor_id: int = 0) -> bool:
        return (
            self.base_repository.db.query(self._entity)
            .filter(self._entity.crm == crm, self._entity.id != doctor_id)
            .first()
            is not None
        )

    def create(self, doctor_data: DoctorCreate):
        if self.crm_exists(doctor_data.crm):
            raise HTTPException(status_code=400, detail="CRM já cadastrado.")
        new_doctor = Doctor(
            name=doctor_data.name,
            specialty=doctor_data.specialty,
            crm=doctor_data.crm
        )
        try:
            return self.base_repository.create(new_doctor)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao criar médico.") from e

    def find_one(self, doctor_id: int):
        doctor = self.base_repository.find_one(self._entity, doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Médico não encontrado.")
        return doctor

    def find_all(self):
        return self.base_repository.find_all(self._entity)

    def update(self, doctor_id: int, doctor_data: DoctorUpdate):
        try:
            doctor = self.base_repository.find_one(self._entity, doctor_id)
            if not doctor:
                raise HTTPException(status_code=404, detail="Médico não encontrado.")
            if doctor_data.crm and self.crm_exists(doctor_data.crm, doctor_id):
                raise HTTPException(status_code=400, detail="CRM já cadastrado.")
            self.base_repository.update_one(self._entity, doctor_id, doctor, doctor_data)
            return self.find_one(doctor_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao atualizar médico.") from e

    def delete(self, doctor_id: int):
        try:
            self.base_repository.delete_one(self._entity, doctor_id)
            return {"message": "Médico removido com sucesso."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao remover médico.") from e


    def find_by_specialty(self, specialty: str):
        return self.base_repository.db.query(self._entity).filter(self._entity.specialty == specialty).all()