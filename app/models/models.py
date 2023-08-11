# como buena práctica importaremos la clase UserMixin que incluiremos en nuestra clase User
# para en caso de ser necesario ahora o en futuros proyectos heredar métodos muy útiles 
# y no tener q implementarlos nosotros.
from flask_login import UserMixin

from datetime import datetime

from app.db import db

#creamos la clase User la cual usará el ORM para crear una tabla en la base de datos Sqlite3
class User(db.Model, UserMixin):
    # nombre de la tabla
    __tablename__ = 'users'

    # columnas
    id = db.Column(db.Integer, primary_key=True)
    date_created_user = db.Column(db.DateTime, default=datetime.now)

    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    admin = db.Column(db.String(5), default='no')
    live = db.Column(db.Integer, default=0)

    # constructor de la clase
    def __init__(self, username, email, password, admin, live) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
        self.live = live