from flask_security.forms import PasswordField, StringField
from flask_wtf import Form
from wtforms import EmailField
from wtforms.widgets import CheckboxInput

class LoginForm(Form):
    email = EmailField('Correo')
    password = PasswordField('Contraseña')
    remember = CheckboxInput('Recordarme')

class RegisterForm(Form):
    name = StringField('Nombre')
    email = EmailField('Correo')
    password = PasswordField('Contraseña')
    confirm_password = PasswordField('Confirmar Contraseña')

