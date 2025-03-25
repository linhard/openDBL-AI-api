from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route("/tokenize", methods=["POST"])
def tokenize():
    data = request.get_json()
    rdf_text = data.get("rdf", "")
    tokens = re.findall(r"\w+", rdf_text)
    return jsonify(tokens=tokens)

@app.route("/", methods=["GET"])
def hello():
    return "Tokenizer API is running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
