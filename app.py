from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime

# Loading Environment Variables
env_path = Path('.') / '.env'
load_dotenv(env_path)

# Creating and Configuring The Flask App
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Old sqlite3 Database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# MySQL DB
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mananbhanushali@localhost/users"

# Initializing the Database
db = SQLAlchemy(app)


# Create Models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Name %r>" % self.name


# Create Form Classes
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def index():
    my_name = "Manan"
    return render_template("index.html", name=my_name)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


@app.route("/name", methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully")

    return render_template("name.html",
                           name=name,
                           form=form)


@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data

        form.name.data = ""
        form.email.data = ""

        flash("User Added Successfully")

    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", form=form, name=name, our_users=our_users)


# Custom Error Pages

# Page Not Found Error
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template("error404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error500.html"), 500
