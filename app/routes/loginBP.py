from app import app
from flask import Blueprint
from app.db import db
from app.models.models import User
from app.forms.forms import LoginForm, RegisterForm
from app import bcrypt, login_manager

from flask import redirect, render_template, url_for, flash
from flask_login import login_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

loginBP = Blueprint('login', __name__)

# ------------------ vistas ------------------#

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('invalid password...')
                return redirect(url_for('login'))
            
        else:
            flash('user not found...')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin='no', live=0)
        db.session.add(new_user)
        db.session.commit()
        flash('registration succesfuly')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)