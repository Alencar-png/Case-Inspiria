from fastapi import Depends, HTTPException
from repositories.base_repository import BaseRepository, CRUDBase
from schemas.scheduling_schemas import SchedulingCreate, SchedulingUpdate
from models.models import Scheduling
import logging

logger = logging.getLogger(__name__)

class SchedulingRepository(CRUDBase):
    def __init__(self, base_repository: BaseRepository = Depends()):
        self.base_repository = base_repository

    @property
    def _entity(self):
        return Scheduling

    def create(self, scheduling_data: SchedulingCreate):
        new_scheduling = Scheduling(
            scheduling_date=scheduling_data.scheduling_date,
            scheduling_time=scheduling_data.scheduling_time,
            scheduling_type=scheduling_data.scheduling_type,
            doctor_id=scheduling_data.doctor_id,
            patient_id=scheduling_data.patient_id,
            rescheduled=scheduling_data.rescheduled
        )
        try:
            return self.base_repository.create(new_scheduling)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao criar agendamento.") from e

    def find_one(self, scheduling_id: int):
        scheduling = self.base_repository.find_one(self._entity, scheduling_id)
        if not scheduling:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        return scheduling

    def find_all(self):
        return self.base_repository.find_all(self._entity)

    def update(self, scheduling_id: int, scheduling_data: SchedulingUpdate):
        try:
            scheduling = self.base_repository.find_one(self._entity, scheduling_id)
            if not scheduling:
                raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
            self.base_repository.update_one(self._entity, scheduling_id, scheduling, scheduling_data)
            return self.find_one(scheduling_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao atualizar agendamento.") from e

    def delete(self, scheduling_id: int):
        try:
            self.base_repository.delete_one(self._entity, scheduling_id)
            return {"message": "Agendamento removido com sucesso."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao remover agendamento.") from e
