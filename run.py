from app import app, csrf
from app.socketio import socketio

if __name__ == '__main__':
    csrf.init_app(app)
    
    # esta es la forma adecuada de usar socketio aqui se puede configurar tambien
    # app, recordemos que ahora entrara en escena el servidor gevent
    socketio.run(app, host='127.0.0.1', port=8080)