from flask import Flask, jsonify
import oracledb
import os
import rdflib

app = Flask(__name__)

# Umgebungsvariablen (oder einfach hier direkt eintragen)
DB_USER = "KLAUS"
DB_PASS = os.getenv("DB_PASS", "!monCarapach0")  # alternativ sicher speichern
DB_DSN = "(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.eu-frankfurt-1.oraclecloud.com))(connect_data=(service_name=gf179da5d49d7ff_graphstudio_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))"

@app.route("/api/blob2clob/<int:id_ontology>", methods=["GET"])
def blob_to_clob(id_ontology):
    try:
        print(f"🔌 Verbinde mit Oracle Autonomous DB für ID {id_ontology} ...")
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN
        )
        cursor = connection.cursor()

        # BLOB auslesen
        cursor.execute("SELECT file_blob FROM eba_demo_files WHERE id = :id", [id_ontology])
        row = cursor.fetchone()
        if not row or not row[0]:
            return jsonify({"status": "error", "message": f"BLOB nicht gefunden für ID {id_ontology}"}), 404

        blob_data = row[0].read()
        clob_text = blob_data.decode("utf-8", errors="replace")

        # RDF/Turtle Validierung
        valid = False
        try:
            g = rdflib.Graph()
            g.parse(data=clob_text, format="turtle")
            valid = True
        except Exception as e:
            print(f"❌ RDF Parsing-Fehler: {e}")
            valid = False

        result = {
            "status": "success",
            "id": id_ontology,
            "valid_rdf": valid,
            "length": len(clob_text),
        }

        return jsonify(result)

    except oracledb.DatabaseError as e:
        error, = e.args
        return jsonify({
            "status": "error",
            "message": f"Datenbankfehler: {error.message}",
            "code": error.code,
            "help": "https://docs.oracle.com/error-help/db/ora-" + str(error.code).zfill(5) + "/"
        }), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
