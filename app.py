from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
my_app_secret_key = os.environ["FLASK_APP_1_SECRET_KEY"]  # Get from my environment for SQLAlchemy

app.config["SECRET_KEY"] = my_app_secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


class Form(db.Model):
    # Specify sqlite db structure
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]  # Name of the input in html
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # Fill the table with sent items
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_object, occupation=occupation)
        db.session.add(form)
        db.session.commit()

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
