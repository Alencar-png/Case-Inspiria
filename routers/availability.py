from fastapi import APIRouter, Depends, HTTPException
from repositories.scheduling_repository import SchedulingRepository
from repositories.doctor_repository import DoctorsRepository
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

availability = APIRouter()

POSSIBLE_TIME_SLOTS = [
    "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00"
]

class SuggestedAppointment(BaseModel):
    date: str
    available_times: List[str]
    suggestion: str
    suggested_date: str
    suggested_time: str

class SuggestedAppointmentRequest(BaseModel):
    doctor_id: int
    start_date: str  # no formato dd/mm/yyyy

@availability.get("/doctors/{doctor_id}/available-times", response_model=List[str])
def get_available_times(
    doctor_id: int,
    date: str,
    sched_repo: SchedulingRepository = Depends(),
    doctor_repo: DoctorsRepository = Depends()
):
    # Valida a existência do médico
    doctor_repo.find_one(doctor_id)
    
    try:
        parsed_date = datetime.strptime(date, '%d/%m/%Y')
        formatted_date = parsed_date.strftime('%d/%m/%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato dd/mm/yyyy")
    
    schedulings = sched_repo.get_schedulings_by_doctor_and_date(doctor_id, formatted_date)
    taken_slots = [s.scheduling_time for s in schedulings]
    available_slots = [slot for slot in POSSIBLE_TIME_SLOTS if slot not in taken_slots]
    return available_slots

@availability.post("/suggested-appointment", response_model=SuggestedAppointment)
def get_suggested_appointment(
    request: SuggestedAppointmentRequest,
    sched_repo: SchedulingRepository = Depends(),
    doctor_repo: DoctorsRepository = Depends()
):
    """
    Sugere o dia mais próximo, a partir da data informada no body,
    com horários disponíveis para o médico especificado.
    Retorna a data sugerida, a lista de horários disponíveis, 
    uma mensagem com o melhor horário e os campos 'suggested_date' e 'suggested_time' separadamente.
    """
    # Valida a existência do médico
    doctor_repo.find_one(request.doctor_id)
    
    try:
        parsed_date = datetime.strptime(request.start_date, '%d/%m/%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato dd/mm/yyyy")
    
    # Busca nos próximos 14 dias por disponibilidade
    for i in range(14):
        candidate_date = parsed_date + timedelta(days=i)
        formatted_date = candidate_date.strftime('%d/%m/%Y')
        schedulings = sched_repo.get_schedulings_by_doctor_and_date(request.doctor_id, formatted_date)
        taken_slots = [s.scheduling_time for s in schedulings]
        available_slots = [slot for slot in POSSIBLE_TIME_SLOTS if slot not in taken_slots]
        
        if available_slots:
            suggested_date = formatted_date
            suggested_time = available_slots[0]
            suggestion = f"O melhor horário que tenho disponível para você é {suggested_date} às {suggested_time}"
            return SuggestedAppointment(
                date=formatted_date,
                available_times=available_slots,
                suggestion=suggestion,
                suggested_date=suggested_date,
                suggested_time=suggested_time
            )
    
    raise HTTPException(status_code=404, detail="Não há horários disponíveis nos próximos 14 dias.")
