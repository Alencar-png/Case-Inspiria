from fastapi import Depends, HTTPException, Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from repositories.base_repository import BaseRepository, CRUDBase
from schemas.patient_schemas import PatientCreate, PatientUpdate
from models.models import Patient
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for request {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

class PatientsRepository(CRUDBase):
    def __init__(self, base_repository: BaseRepository = Depends()):
        self.base_repository = base_repository

    @property
    def _entity(self):
        return Patient

    def cpf_exists(self, cpf: str, patient_id: int = 0) -> bool:
        return (
            self.base_repository.db.query(self._entity)
            .filter(self._entity.cpf == cpf, self._entity.id != patient_id)
            .first()
            is not None
        )

    def find_by_cpf(self, cpf: str):
        return self.base_repository.db.query(self._entity).filter(self._entity.cpf == cpf).first()

    def create(self, patient_data: PatientCreate):
        if self.cpf_exists(patient_data.cpf):
            raise HTTPException(status_code=400, detail="CPF já cadastrado.")
        new_patient = Patient(
            name=patient_data.name,
            cpf=patient_data.cpf,
            birth_date=patient_data.birth_date,
            phone=patient_data.phone,
            health_insurance=patient_data.health_insurance,
            photo=patient_data.photo
        )
        try:
            return self.base_repository.create(new_patient)
        except Exception as e:
            logger.error("Erro ao criar paciente", exc_info=True)
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
            if patient_data.cpf and self.cpf_exists(patient_data.cpf, patient_id):
                raise HTTPException(status_code=400, detail="CPF já cadastrado.")
            self.base_repository.update_one(self._entity, patient_id, patient, patient_data)
            return self.find_one(patient_id)
        except Exception as e:
            logger.error("Erro ao atualizar paciente", exc_info=True)
            raise HTTPException(status_code=500, detail="Erro ao atualizar paciente.") from e

    def delete(self, patient_id: int):
        try:
            self.base_repository.delete_one(self._entity, patient_id)
            return {"message": "Paciente removido com sucesso."}
        except Exception as e:
            logger.error("Erro ao remover paciente", exc_info=True)
            raise HTTPException(status_code=500, detail="Erro ao remover paciente.") from e
