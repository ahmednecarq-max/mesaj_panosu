from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# API servisinin adresi — deploy sonrası güncellenecek
API_URL = os.getenv("API_URL", "http://localhost:5001")

HTML = """
<!doctype html>
<html>
<head>
    <title>Anonim Mesaj Panosu</title>
    <style>
        body { font-family: Arial; text-align: center;
               padding: 40px; background: #f0f4ff; }
        h1   { color: #333; }
        textarea { width: 300px; height: 80px;
                   font-size: 15px; padding: 8px; }
        button { display: block; margin: 10px auto;
                 padding: 10px 20px; background: #5B6EF5;
                 color: white; border: none;
                 border-radius: 6px; cursor: pointer; }
        .kart { background: white; margin: 8px auto;
                width: 320px; padding: 12px;
                border-radius: 8px; text-align: left;
                box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
        .zaman { font-size: 11px; color: #aaa; }
    </style>
</head>
<body>
    <h1>📌 Anonim Mesaj Panosu</h1>
    <p>İsim vermeden mesajını bırak!</p>

    <form method="POST">
        <textarea name="mesaj" placeholder="Mesajını yaz..." required></textarea>
        <button type="submit">Gönder</button>
    </form>

    <h3>Mesajlar (Son 10):</h3>
    {% for m in mesajlar %}
        <div class="kart">
            {{ m.mesaj }}
            <div class="zaman">{{ m.zaman }}</div>
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():

    # Yeni mesaj geldiyse API'ye gönder
    if request.method == "POST":
        mesaj = request.form.get("mesaj")
        if mesaj:
            requests.post(
                f"{API_URL}/mesajlar",
                json={"mesaj": mesaj}
            )

    # Mesajları API'den al
    cevap = requests.get(f"{API_URL}/mesajlar")
    mesajlar = cevap.json()

    return render_template_string(HTML, mesajlar=mesajlar)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
