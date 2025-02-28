from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from repositories.scheduling_repository import SchedulingRepository
from schemas.scheduling_schemas import SchedulingCreate, SchedulingUpdate, SchedulingResponse
from typing import List
from uuid import UUID
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

scheduling = APIRouter()

@scheduling.post("/schedulings/", status_code=HTTPStatus.CREATED, response_model=SchedulingResponse)
def create_scheduling(scheduling_data: SchedulingCreate, repo: SchedulingRepository = Depends()):
    return repo.create(scheduling_data)

@scheduling.get("/schedulings/", response_model=List[SchedulingResponse])
def read_schedulings(repo: SchedulingRepository = Depends()):
    return repo.find_all()

@scheduling.get("/schedulings/{scheduling_id}", response_model=SchedulingResponse)
def read_scheduling(scheduling_id: UUID, repo: SchedulingRepository = Depends()):
    return repo.find_one(scheduling_id)

@scheduling.put("/schedulings/{scheduling_id}", response_model=SchedulingResponse)
def update_scheduling(scheduling_id: UUID, scheduling_data: SchedulingUpdate, repo: SchedulingRepository = Depends()):
    return repo.update(scheduling_id, scheduling_data)

@scheduling.delete("/schedulings/{scheduling_id}")
def delete_scheduling(scheduling_id: UUID, repo: SchedulingRepository = Depends()):
    return repo.delete(scheduling_id)
