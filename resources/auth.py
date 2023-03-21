from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import LoginForm, current_user, login_user, login_required, logout_user
from forms import RegisterForm
from models import User
from db import db
from security import user_datastore

blp = Blueprint('auth', __name__)


@blp.get('/register')
def register():
    form = RegisterForm()
    return render_template('auth/register.html', form = form)

@blp.post('/register')
def create_user():
    form = RegisterForm(request.form)
    user = User.query.filter_by(email=form.email.data).first()

    if user:
        flash('El correo electrónico ya existe')
        return redirect(url_for('auth.register'))

    new_user = user_datastore.create_user(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='sha256'),
            )
    db.session.commit()

    login_user(new_user)

    return redirect(url_for('main.index'))

@blp.get('/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', form = form)

@blp.post('/login')
def create_session():
    form = LoginForm(request.form)
    user = User.query.filter_by(email = form.email.data).first()
    if not user or not check_password_hash(user.password, form.password.data):
        flash('El usuario o la contraseña son incorrectos')
        return redirect(url_for('auth.login'))

    login_user(user)
    
    if user.has_role('admin'):
        return redirect(url_for('admin.index'))

    return redirect(url_for('main.index'))

@blp.post('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
