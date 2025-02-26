from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, deferred
from config.database import Base

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

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    crm = Column(String, nullable=False, unique=True)