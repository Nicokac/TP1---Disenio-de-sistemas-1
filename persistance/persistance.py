from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Crear carpetas 'usuarios' y 'registros' si no existen
if not os.path.exists('usuarios'):
    os.makedirs('usuarios')
if not os.path.exists('registros'):
    os.makedirs('registros')

# Crear el motor de la base de datos para usuarios
user_db_filename = 'usuarios.db'
user_db_filepath = os.path.join('usuarios', user_db_filename)
user_engine = create_engine(f'sqlite:///{user_db_filepath}', echo=True)

# Crear el motor de la base de datos para registros con la fecha en el nombre del archivo
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
registros_db_filename = f'registros_{timestamp}.db'
registros_db_filepath = os.path.join('registros', registros_db_filename)
registros_engine = create_engine(f'sqlite:///{registros_db_filepath}', echo=True)

# Crear una clase base para los modelos
Base = declarative_base()

# Crear sesiones
UserSession = sessionmaker(bind=user_engine)
user_session = UserSession()

RegistrosSession = sessionmaker(bind=registros_engine)
registros_session = RegistrosSession()