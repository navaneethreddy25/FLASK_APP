import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

load_dotenv()

API_KEY = os.getenv("NINJA_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

API_URL = "https://api.api-ninjas.com/v1/quotes"

headers = {
    "X-Api-Key": API_KEY
}

app = Flask(__name__)
app.secret_key = "secret123"   # required for session

def generate_ai_quote():
    response = requests.get(API_URL, headers=headers)
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        return data[0]["quote"], data[0]["author"]
    return "No quote received", "Unknown"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("username")
        return redirect(url_for("ai_quotes"))
    return render_template("login.html")

@app.route("/ai")
def ai_quotes():
    if "user" not in session:
        return redirect(url_for("login"))

    quote, author = generate_ai_quote()
    return render_template("index.html", quote=quote, author=author)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
