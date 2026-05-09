import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

def chat_with_PepetGPT(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(e)
        return f"AI Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@limiter.limit("5 per minute")
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Request tidak valid"}), 400

    user_message = data["message"].strip()

    if not user_message:
        return jsonify({"error": "Pesan kosong"}), 400

    if len(user_message) > 2000:
        return jsonify({"error": "Pesan terlalu panjang"}), 400

    reply = chat_with_PepetGPT(user_message)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)