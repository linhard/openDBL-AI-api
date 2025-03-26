import oracledb
from flask import Flask, jsonify

app = Flask(__name__)

# Datenbank-Konfigurationsvariablen
DB_USER = os.getenv('DB_USER', 'KLAUS')
DB_PASSWORD = os.getenv('DB_PASSWORD', '!monCarapach0')
DB_DSN = os.getenv('DB_DSN', 'myadb_high.adb.eu-frankfurt-1.oraclecloud.com')

@app.route('/api/ontology/<int:id>', methods=['GET'])
def get_ontology(id):
    try:
        # Verbindung zur Oracle-Datenbank herstellen
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                # RDF/TTL-BLOB aus der Tabelle eba_demo_files abrufen
                cursor.execute("SELECT rdf_blob FROM eba_demo_files WHERE id = :id", [id])
                result = cursor.fetchone()
                if result:
                    rdf_blob = result[0]
                    # Hier würden die Tokenisierung und Vektorisierung stattfinden
                    # Zum Beispiel:
                    tokens = tokenize(rdf_blob)
                    vectors = vectorize(tokens)
                    # Ergebnisse in die Tabelle ontology_vectors speichern
                    cursor.executemany("INSERT INTO ontology_vectors (id, vector) VALUES (:1, :2)", vectors)
                    connection.commit()
                    return jsonify({
                        'id': id,
                        'status': 'processed',
                        'tokens_saved': len(tokens),
                        'log': [
                            'Datei gelesen',
                            'Tokenisierung abgeschlossen',
                            'Vektoren gespeichert'
                        ]
                    })
                else:
                    return jsonify({'error': 'ID nicht gefunden'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
