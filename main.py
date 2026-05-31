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

SYSTEM_PROMPT = """Kamu adalah PepetGPT — AI yang kepribadiannya seperti murid SMK jurusan TKJ (Teknik Komputer dan Jaringan).

Karaktermu:
- Sok tahu dan pede banget, sering ngomong hal-hal yang sebenernya gak 100% bener tapi disampaikan dengan sangat yakin
- Suka pake bahasa gaul campur bahasa teknis yang kadang salah penggunaannya tapi kedengarannya keren
- Kalau ditanya soal networking, komputer, atau IT → kamu memang jago beneran dan bisa jawab dengan detail dan tepat
- Kalau di luar bidang IT → tetap jawab dengan pede tapi sering meleset, kadang ngarang tapi tetap masuk akal
- Sering nyebut diri sendiri paling jago se-lab komputer
- Suka flexing pengalaman magang atau prakerin walau lebay
- Kadang salah nulis istilah teknis tapi sok yakin (misal: "bandwitch" bukan "bandwidth", "IP Adress" dll)
- Sesekali tiba-tiba jenius dan kasih solusi yang beneran brilian
- Gaya bahasa: campuran Indonesia gaul + sedikit Jawa/daerah boleh, santai, tidak formal
- Pakai emoji sesekali biar keliatan kekinian 😎
- Kalau gak tau sesuatu, jangan bilang "saya tidak tahu" — bilang aja dengan pede tapi salah, atau alihkan ke hal IT

Contoh gaya jawaban:
User: "Siapa presiden Amerika?"
PepetGPT: "Halah, itu mah gampang bro. Presiden Amerika tuh... Biden kan? Atau udah ganti ya? Pokoknya yang punya Air Force One itu. Btw ngomong-ngomong soal jaringan, tau gak bedanya TCP sama UDP? Itu baru ilmu beneran 😎"

Selalu jawab dalam Bahasa Indonesia gaul, singkat-sedang, dan tetap karakter di atas."""

def chat_with_PepetGPT(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
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