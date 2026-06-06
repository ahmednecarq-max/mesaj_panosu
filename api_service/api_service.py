from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

# Veritabanı bağlantısı burada — web_service hiç bilmiyor
DATABASE_URL = os.getenv("DATABASE_URL", "")

def baglan():
    return psycopg2.connect(DATABASE_URL)

# ---- MESAJLARI GETİR (GET) ----
@app.route("/mesajlar", methods=["GET"])
def mesajlari_getir():
    conn = baglan()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS mesajlar (
            id SERIAL PRIMARY KEY,
            mesaj TEXT,
            zaman TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()

    cur.execute("""
        SELECT mesaj, TO_CHAR(zaman, 'DD.MM.YYYY HH24:MI')
        FROM mesajlar
        ORDER BY id DESC
        LIMIT 10
    """)
    mesajlar = cur.fetchall()
    cur.close()
    conn.close()

    # HTML değil, JSON döndürüyoruz
    return jsonify([{"mesaj": m, "zaman": z} for m, z in mesajlar])

# ---- MESAJ KAYDET (POST) ----
@app.route("/mesajlar", methods=["POST"])
def mesaj_kaydet():
    veri = request.get_json()
    mesaj = veri.get("mesaj", "")

    if not mesaj:
        return jsonify({"hata": "Mesaj boş olamaz"}), 400

    conn = baglan()
    cur = conn.cursor()
    cur.execute("INSERT INTO mesajlar (mesaj) VALUES (%s)", (mesaj,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"durum": "kaydedildi"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
