import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai
from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

google.generativeai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = google.generativeai.GenerativeModel("gemma-3-27b-it")


app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

def chat_with_PepetGPT(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()



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

@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Allow: /
Sitemap: https://pepetgpt.obr.my.id/sitemap.xml
''', 200, {'Content-Type': 'text/plain'}
##hello



if __name__ == "__main__":
    app.run(debug=True)

