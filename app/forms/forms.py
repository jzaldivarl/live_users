# Importamos FlaskForm para crear formularios de forma segura
# del cual heredaran nuestras clases LoginForm y RegisterForm que
# usaremos para construir nuestro sistema de login vale destacar
# que acepta estilos css
from flask_wtf import FlaskForm

# para definir el tipo de input de los campos que vamos a usar
# y validar los datos entrados por teclado
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, ValidationError

from app.models.models import User

# formulario login
class LoginForm(FlaskForm):
    username = StringField(validators=
                           [input_required()], render_kw={"placeholder": "username"})
    password = PasswordField(validators=
                           [input_required()], render_kw={"placeholder": "password"})
    submit = SubmitField('Login')
    


# formulario signup
class RegisterForm(FlaskForm):
    username = StringField(validators=
                           [input_required()], render_kw={"placeholder": "username"})
    email = StringField(validators=
                           [input_required()], render_kw={"placeholder": "username@gmail.com"})
    password = PasswordField(validators=
                           [input_required()], render_kw={"placeholder": "password"})
    submit = SubmitField('Signup')

    # método de clase
    def validate_username(self, username):
        existing_user_name = User.query.filter_by(username=username.data).first()
        if existing_user_name:
            raise ValidationError('the username already exists')