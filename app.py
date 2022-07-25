from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path
from os import environ
from flask_migrate import Migrate
from rq.job import Job
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login

app = Flask(__name__)

database = environ.get('DATABASE')
database_user = environ.get('DATABASE_USER')
database_password = environ.get('DATABASE_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@localhost/{}'.format(database_user, database_password, database)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.init_app(app)
login.init_app(app)
login.login_view = 'login'

@app.before_first_request
def create_all():
    db.create_all()

@app.route('/blogs')
@login_required
def blog():
    return render_template('blog.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/blogs')

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/blogs')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/blogs')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/blogs')

if __name__ == "__main__":
    app.run(debug=True)
