from repositories.base_repository import BaseRepository, CRUDBase
from schemas.patient_schemas import PatientCreate, PatientUpdate
from fastapi import Depends, HTTPException
from models.models import Patient

class PatientsRepository(CRUDBase):
    def __init__(self, base_repository: BaseRepository = Depends()):
        self.base_repository = base_repository

    @property
    def _entity(self):
        return Patient

    def create(self, patient_data: PatientCreate):
        new_patient = Patient(
            name=patient_data.name,
            cpf=patient_data.cpf,
            birth_date=patient_data.birth_date,
            phone=patient_data.phone,
            health_insurance=patient_data.health_insurance
        )
        try:
            return self.base_repository.create(new_patient)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao criar paciente.") from e

    def find_one(self, patient_id: int):
        patient = self.base_repository.find_one(self._entity, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente não encontrado.")
        return patient

    def find_all(self):
        return self.base_repository.find_all(self._entity)

    def update(self, patient_id: int, patient_data: PatientUpdate):
        try:
            patient = self.base_repository.find_one(self._entity, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail="Paciente não encontrado.")
            self.base_repository.update_one(self._entity, patient_id, patient, patient_data)
            return self.find_one(patient_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao atualizar paciente.") from e

    def delete(self, patient_id: int):
        try:
            self.base_repository.delete_one(self._entity, patient_id)
            return {"message": "Paciente removido com sucesso."}
        except Exception:
            raise HTTPException(status_code=500, detail="Erro ao remover paciente.")

    def find_by_cpf(self, cpf: str):
        # Aqui é que realizamos a busca filtrada pelo CPF
        patient = self.base_repository.db.query(self._entity).filter(
            self._entity.cpf == cpf
        ).first()
        return patient