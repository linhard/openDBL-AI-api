import os
import oracledb
from flask import Flask, jsonify
import numpy as np
import datetime

app = Flask(__name__)

# ENV-Variablen von Render
DB_USER = os.getenv("DB_USER", "KLAUS")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DSN = os.getenv("DB_DSN")

# Dummy-Tokenisierung (später ersetzbar)
def tokenize(text):
    tokens = set()
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("@"):
            continue
        tokens.update(line.strip().split())
    return list(tokens)

# Dummy-Vektorisierung
def vectorize(tokens, dim=8):
    return np.random.rand(len(tokens), dim).tolist()

# ✅ Root-Route für Render-Verfügbarkeit
@app.route("/")
def index():
    return "Ontology Tokenizer API is live ✅"

# 🧠 Haupt-Endpunkt zur Verarbeitung
@app.route("/api/ontology/<int:file_id>", methods=["GET"])
def process(file_id):
    log = []
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT file_blob FROM eba_demo_files WHERE id = :id", {"id": file_id})
                row = cur.fetchone()
                if not row or not row[0]:
                    return jsonify({"error": "Datei nicht gefunden"}), 404

                rdf_text = row[0].read().decode("utf-8")
                log.append("Datei gelesen")

                tokens = tokenize(rdf_text)
                vectors = vectorize(tokens)
                log.append(f"{len(tokens)} Tokens extrahiert & vektorisiert")

                for i, token in enumerate(tokens):
                    cur.execute("""
                        INSERT INTO ontology_vectors (file_id, token, vector, created_at)
                        VALUES (:file_id, :token, :vector, :created_at)
                    """, {
                        "file_id": file_id,
                        "token": token,
                        "vector": str(vectors[i]),
                        "created_at": datetime.datetime.now()
                    })

                conn.commit()
                log.append("Vektoren gespeichert")

        return jsonify({
            "id": file_id,
            "status": "processed",
            "tokens_saved": len(tokens),
            "log": log
        })

    except Exception as e:
        log.append(f"Fehler: {str(e)}")
        return jsonify({"error": str(e), "log": log}), 500

# ✅ Dynamisches Port-Binding für Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

