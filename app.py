from flask import Flask, render_template, request
from pymongo import MongoClient
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

app = Flask(__name__)

 # MongoDB Connection
client = MongoClient(
    "mongodb+srv://codealpha:Rutvik1234@codealpha.pcamknc.mongodb.net/?appName=codealpha"
)

db = client["CodeAlphaDB"]
collection = db["users"] 


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()

        # Email Validation
        try:
            validate_email(email)

        except EmailNotValidError:

            return render_template(
                "index.html",
                message="Invalid Email Address"
            )

        # Duplicate Name Check
        existing_name = collection.find_one(
            {"name": name}
        )

        # Duplicate Email Check
        existing_email = collection.find_one(
            {"email": email}
        )

        if existing_name:

            message = "Duplicate Name Found"

        elif existing_email:

            message = "Email Already Exists"

        else:

            collection.insert_one({

                "name": name,
                "email": email,
                "created_at": datetime.utcnow()

            })

            message = "Data Added Successfully"

    return render_template(
        "index.html",
        message=message
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )