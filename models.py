from sqlalchemy import Column, Integer, String, Float
from database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    edad = Column(Integer)
    correo = Column(String)
    promedio = Column(Float)
    