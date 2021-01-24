from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
	my_name = "Manan"
	return render_template("index.html", name=my_name)


@app.route("/user/<name>")
def user(name):
	return render_template("user.html", user_name=name)
    # return f"<h1>Hello {name}</h1>"	
