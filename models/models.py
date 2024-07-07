from sqlalchemy import Column, Integer, String
from persistance.persistance import Base

class Registro(Base):
    __tablename__ = 'registros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    nombre_materia = Column(String)
    nota = Column(String)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True)
    password = Column(String)