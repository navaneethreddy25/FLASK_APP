import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

API_KEY = os.getenv("NINJA_API_KEY")

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

@app.route("/")
def home():
    quote, author = generate_ai_quote()
    return render_template(
        "index.html",
        quote=quote,
        author=author
    )

if __name__ == "__main__":
    app.run(debug=True)