from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from pathlib import Path
import os

# Loading Environment Variables
env_path = Path('.') / '.env'
load_dotenv(env_path)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# Create A Form Class
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


# Custom Error Pages

# Page Not Found Error
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template("error404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error500.html"), 500
