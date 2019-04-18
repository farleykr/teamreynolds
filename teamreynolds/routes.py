from flask import render_template, url_for, flash, redirect, request
from teamreynolds import app, db, bcrypt
from teamreynolds.models import User
from teamreynolds.forms import RegistrationForm, LoginForm, UploadPictureForm
from flask_login import login_user, logout_user, current_user, login_required
import os
import secrets


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path + '/static/images', picture_fn)
    form_picture.save(picture_path)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = UploadPictureForm()
    image_files = []
    if form.validate_on_submit():
        if form.picture.data:
            save_picture(form.picture.data)
        return redirect(url_for('index'))
    for image_file in os.listdir(os.path.join(os.path.dirname(__file__) + url_for('static', filename='images/'))):
        image_files.append(image_file)
    return render_template('index.html', form=form, image_files=image_files)


@app.route("/about")
@login_required
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.  You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
