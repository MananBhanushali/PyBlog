from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    my_name = "Manan"
    return render_template("index.html", name=my_name)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


# Custom Error Pages

# Page Not Found Error
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template("error404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error500.html"), 500
