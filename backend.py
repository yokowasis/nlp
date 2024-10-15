from flask import Flask, request, jsonify
from flask_cors import CORS
from fn import encode, summarize, translate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Sample data
data = {
    "hello": "world",
    "man": [
        "aaa", "bbb", "ccc"
    ]
}

# POST request handler


@app.route("/api/vectorize", methods=['POST'])
def api_vectorize():
    inputs = request.get_json()
    vec = encode(inputs['text'])
    return jsonify(vec)


@app.route("/api/summarize", methods=['POST'])
def api_summarize():
    inputs = request.get_json()
    summary = summarize(inputs['text'])
    return jsonify(summary)


@app.route("/api/translate", methods=['POST'])
def api_translate():
    inputs = request.get_json()
    translation = translate(inputs['text'])
    return jsonify(translation)


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)


@app.route('/', methods=['GET'])
def get_index():
    return """
    <pre>
    Usage :
    POST /api/vectorize
    {
        "text": "hello world"
    }
    
    POST /api/summarize
    {
        "text": "hello world"
    }

    POST /api/translate
    {
        "text": "Halo Dunia"
    }

    </pre>
"""


debugenv = os.getenv('DEBUG')
if debugenv == "True":
    app.run(host="localhost", debug=True,
            port=int(os.getenv('PORT') or "3012"))
else:
    from waitress import serve
    serve(app, host="localhost", port=int(os.getenv('PORT') or "8080"))
