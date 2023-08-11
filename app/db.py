# importamos del módulo general __init__.py a app
from app import app

# explotaremos el ORM SQLAlchemy para oprerar mas facil sobre base de datos sqlite3
# que es el tipo de base de datos que usaremos en este proyecto.
# cortesía de flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# creamos una instancia y le pasamos como parámetro a app
db = SQLAlchemy(app)