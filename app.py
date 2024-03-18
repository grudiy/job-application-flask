from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
my_app_secret_key = os.environ["FLASK_APP_1_SECRET_KEY"]  # Get from my environment for SQLAlchemy
MAIL_PASS = os.environ["GMAIL_APP_GRUANDAPP_KEY"] # Get my gmail app pass from environment

app.config["SECRET_KEY"] = my_app_secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Add gmail sending parameters
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "gruandapp@gmail.com"
app.config["MAIL_PASSWORD"] = MAIL_PASS

db = SQLAlchemy(app)

mail = Mail(app)

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

        message_body = (f"Dear {first_name} {last_name}."
                        f"Thank you for your submission!\n"
                        f"We've received your data:\n"
                        f"{first_name}\n{last_name}\n{date}\n{occupation}")

        message = Message(subject="Flask job application form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email, "gruand+333@gmail.com"],
                          body=message_body)

        mail.send(message)
        # Success message (jinja 2 in html)
        flash(f"Thank you {first_name}! Your form was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
