from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path
from os import environ
from flask_migrate import Migrate
from rq.job import Job

app = Flask(__name__)

database = environ.get('DATABASE')
database_user = environ.get('DATABASE_USER')
database_password = environ.get('DATABASE_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@localhost/{}'.format(database_user, database_password, database)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
