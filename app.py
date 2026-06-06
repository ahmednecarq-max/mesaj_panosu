from flask import Flask, render_template_string, request
import os
import psycopg2

app = Flask(__name__)

# Veritabanı bağlantı adresi ortam değişkeninden okunuyor
DATABASE_URL = os.getenv("DATABASE_URL", " ")

# ---- HTML ŞABLONU ----
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
    {% for m, z in mesajlar %}
        <div class="kart">
            {{ m }}
            <div class="zaman">{{ z }}</div>
        </div>
    {% endfor %}
</body>
</html>
"""

# ---- VERİTABANI BAĞLANTISI ----
def baglan():
    return psycopg2.connect(DATABASE_URL)

# ---- ANA SAYFA ----
@app.route("/", methods=["GET", "POST"])
def index():
    conn = baglan()
    cur = conn.cursor()

    # Tablo yoksa oluştur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mesajlar (
            id SERIAL PRIMARY KEY,
            mesaj TEXT,
            zaman TIMESTAMP DEFAULT NOW()
        )
    """)

    # Yeni mesaj geldiyse kaydet
    if request.method == "POST":
        mesaj = request.form.get("mesaj")
        if mesaj:
            cur.execute(
                "INSERT INTO mesajlar (mesaj) VALUES (%s)", (mesaj,)
            )
            conn.commit()

    # Son 10 mesajı getir
    cur.execute("""
        SELECT mesaj, TO_CHAR(zaman, 'DD.MM.YYYY HH24:MI')
        FROM mesajlar
        ORDER BY id DESC
        LIMIT 10
    """)
    mesajlar = cur.fetchall()

    cur.close()
    conn.close()

    return render_template_string(HTML, mesajlar=mesajlar)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
