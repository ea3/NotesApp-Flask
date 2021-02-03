from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('get')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', 'success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password. Try again', 'error')
        else:
            flash('Email does not exist', 'error')

    data = request.form
    print(data)
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'error')
        elif len(email) < 4:
            flash('Email must be grater than 3 chars', 'error')
        elif len(first_name) < 2:
            flash('First name should be at least one char long', 'error')
        elif password1 != password2:
            flash('Passwords do not match', 'error')
        elif len(password1) > 7:
            flash('Password must be greater than 6 characters', 'error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', 'success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')
