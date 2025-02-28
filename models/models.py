from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, deferred
from config.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = deferred(Column(String, nullable=False))
    is_admin = Column(Boolean, nullable=False)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    birth_date = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    health_insurance = Column(Boolean, nullable=False)
    photo = Column(String, nullable=True) 
    
    schedulings = relationship("Scheduling", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    crm = Column(String, nullable=False, unique=True)
    
    schedulings = relationship("Scheduling", back_populates="doctor")

class Scheduling(Base):
    __tablename__ = "schedulings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheduling_date = Column(String, nullable=False)
    scheduling_time = Column(String, nullable=False)
    scheduling_type = Column(String, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    rescheduled = Column(Boolean, nullable=False)
    
    doctor = relationship("Doctor", back_populates="schedulings")
    patient = relationship("Patient", back_populates="schedulings")
