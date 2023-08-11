# módulo general del framework para instanciar nuestra app
from flask import Flask

# para trabajar con las vistas y funciones
from flask import redirect, url_for, render_template

# para el login
from flask_login import current_user, login_required, logout_user, LoginManager

# seguridad para formularios
from flask_wtf import CSRFProtect

# para encriptar passwords de los usuarios
from flask_bcrypt import Bcrypt

# instanciamos nuestra app y le decimos a Flask por cual nombre sera llamada
app = Flask(__name__)
# en este caso "app" pasando el módulo __name__.py como argumento.

# configuración de la app que será heredada de la clase 'DevConfig' del módulo config.py
app.config.from_object('config.DevConfig')

csrf = CSRFProtect()

# instanciamos Bcrypt y le pasamos como argumento a app
bcrypt = Bcrypt(app)

# instanciamos LoginManager y le pasamos como argumento a app y la vista login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ------- Blueprint hacia el modulo loginBP.py que renderiza login.html y signup.html -------#
from app.routes.loginBP import loginBP
app.register_blueprint(loginBP)

# ------------------------- vista home.html -------------------------#
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# ---------------------- vista dashboard.html -----------------------#
@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    if current_user.admin == 'admin':
        return render_template('dashboard.html')
    else:
        return redirect(url_for('home'))

# ----------------------- cerrar sesión ------------------------#
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))