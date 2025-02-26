from fastapi import APIRouter, Depends, HTTPException
from repositories.scheduling_repository import SchedulingRepository
from repositories.doctor_repository import DoctorsRepository
from typing import List
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

availability = APIRouter()

POSSIBLE_TIME_SLOTS = [
    "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00"
]

@availability.get("/doctors/{doctor_id}/available-times", response_model=List[str])
def get_available_times(
    doctor_id: int,
    date: str,
    sched_repo: SchedulingRepository = Depends(),
    doctor_repo: DoctorsRepository = Depends()
):
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
