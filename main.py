import os
from dotenv import load_dotenv
from google import genai
from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

# API Gemini
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

app = Flask(__name__)

# Rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

# Fungsi chat AI
def chat_with_PepetGPT(prompt):
    try:
        print("PROMPT:", prompt)

        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=prompt
        )

        print("RESPONSE:", response)

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "AI tidak memberi jawaban."

    except Exception as e:
        import traceback
        traceback.print_exc()

        return f"ERROR: {str(e)}"

# Halaman utama
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint chat
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

# Sitemap
@app.route('/sitemap.xml')
def sitemap():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://pepetgpt.obr.my.id/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>''', 200, {'Content-Type': 'application/xml'}

# Robots
@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Allow: /
Sitemap: https://pepetgpt.obr.my.id/sitemap.xml
''', 200, {'Content-Type': 'text/plain'}

# Run Flask
if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)

