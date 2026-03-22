import google.generativeai
from flask import Flask, render_template, request, jsonify


google.generativeai.configure(api_key="GEMINI_API_KEY")
model = google.generativeai.GenerativeModel("gemini-robotics-er-1.5-preview")


app = Flask(__name__)
def chat_with_PepetGPT(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]
    reply = chat_with_PepetGPT(user_message)
    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=True)

