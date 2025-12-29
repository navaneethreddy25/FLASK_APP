import requests
import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask, render_template,request
from flask_mysqldb import MySQL

load_dotenv()
API_KEY = os.getenv("NINJA_API_KEY")
con = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
    )
cursor = con.cursor()

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

API_URL = "https://api.api-ninjas.com/v1/quotes"

headers = {
    "X-Api-Key": API_KEY
}

app = Flask(__name__)

def generate_ai_quote():
    response = requests.get(API_URL, headers=headers)
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        quote = data[0]["quote"]
        author = data[0]["author"]
        return quote, author
    else:
        return "No quote received", "Unknown"

@app.route("/ai")
def index():
    quote, author = generate_ai_quote()
    return render_template(
        "index.html",
        quote=quote,
        author=author
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registration', methods=['GET','POST'])
def registration():
    if request.method == "POST":
        user = request.form["username"]
        email = request.form['email']
        password = request.form['password']
        cursor.execute("insert into registration(username,email,password) values (%s,%s,%s)", [user,email,password])
        con.commit()
        return "values stored"
    return render_template('registration.html') 

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)