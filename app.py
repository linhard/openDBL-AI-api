import os
from flask import Flask, jsonify
import oracledb
from rdflib import Graph
from dotenv import load_dotenv

# 🔐 .env laden
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

app = Flask(__name__)

@app.route("/api/blob2clob/<int:id_ontology>", methods=["GET"])
def blob2clob(id_ontology):
    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = connection.cursor()

        cursor.execute("SELECT file_blob FROM eba_demo_files WHERE id = :id", {"id": id_ontology})
        row = cursor.fetchone()

        if not row or not row[0]:
            return jsonify({"status": "error", "message": "No BLOB found for this ID"}), 404

        blob_data = row[0].read()
        ttl_text = blob_data.decode("utf-8")

        # ✅ RDF-Syntaxprüfung
        g = Graph()
        try:
            g.parse(data=ttl_text, format="turtle")
            is_valid = True
            error_msg = ""
        except Exception as e:
            is_valid = False
            error_msg = str(e)

        result = {
            "id": id_ontology,
            "status": "success" if is_valid else "invalid",
            "valid_rdf": is_valid,
            "length": len(ttl_text),
            "rdf_text": ttl_text
        }

        if not is_valid:
            result["validation_error"] = error_msg

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Datenbankfehler: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
