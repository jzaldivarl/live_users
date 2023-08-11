# modulo para base de datos
import sqlite3

from flask_login import current_user

# esta es la libreria mas importante para este modulo del proyecto
from flask_socketio import SocketIO, emit

# importamos del modulo principal app
from app import app

# para base de datos ORM etc
from app.db import db
from app.models.models import User

# creamos un objeto SocketIO para manejar eventos y comunicacion cliente-servidor
# y le damos una configuracion
socketio = SocketIO(
    app,
    logger=True,
    engineio_logger=True
)

# vamos a crear una lista vacia ya veran
users_data = []

# cliente que cargue una pagina tendra comunicacion con el servidor o sea aca en el backend
# este claro estara escuchando y emitira a su vez otra hacia el cliente
@socketio.on('connect')
def users_connect():
    # llamada global a la lista
    global users_data

    # aqui se recorre la lista y se adiciona una unica vez si el usuario no esta en ella
    if users_data.count(current_user.id) == 0:
        users_data.append(current_user.id)

        try:
            user_to_update = User.query.get_or_404(current_user.id)
            user_to_update.live = 1
            db.session.commit()

            # observaremos en la terminal para checkear
            print('==========\n\n\tusuario conectado\n\n==========')

            # en este caso utilizaremos sentencias sqlite en vez de usar el ORM
            # no solo por las condiciones de nuestra consulta si no tambien aprovechando
            # la funcion COUNT de sql para de una vez obtener lo que buscamos en menos lineas de codigo
            con = sqlite3.connect('app/database.db')
            cur = con.cursor()
            cur.execute("SELECT COUNT(username) FROM users WHERE (live == 1 AND admin != 'admin')")
            all_data = cur.fetchall()
            con.close()

            # ahora usaremos el metodo emit de soccketio y le pasaremos en su segundo parametro
            # a all_data
            emit('user', all_data, broadcast=True)

        except:
            print('\n\nError al guardar al usuario\n\n')

    else:
        print('el usuario con id:', current_user.id, 'ya esta registrado')


# cliente que reconecte vaya a cargar hacia otra pagina o mas interesante para estos casos
# cierre la ventana del navegador lo captara el cleinte y emitira la informacio aca al servidor
# o sea al backend
@socketio.on('disconnect')
def users_disconnect():
    # llamada global a la lista
    global users_data

    # aqui se recorre la lista para eliminar al usuario desconectado
    for id in users_data:
        if current_user.id == id:
            live = users_data.remove(id)

    try:
            user_to_update = User.query.get_or_404(current_user.id)
            user_to_update.live = 0
            db.session.commit()

            # observaremos en la terminal para checkear
            print('==========\n\n\tusuario desconectado\n\n==========')

            # en este caso utilizaremos sentencias sqlite en vez de usar el ORM
            # no solo por las condiciones de nuestra consulta si no tambien aprovechando
            # la funcion COUNT de sql para de una vez obtener lo que buscamos en menos lineas de codigo
            con = sqlite3.connect('app/database.db')
            cur = con.cursor()
            cur.execute("SELECT COUNT(username) FROM users WHERE (live == 1 AND admin != 'admin')")
            all_data = cur.fetchall()
            con.close()

            # ahora usaremos el metodo emit de soccketio y le pasaremos en su segundo parametro
            # a all_data
            emit('user', all_data, broadcast=True)

    except:
            print('\n\nError al borrar al usuario\n\n')