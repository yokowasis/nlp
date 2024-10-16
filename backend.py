from flask import Flask, request, jsonify
from flask_cors import CORS
from fn import encode, summarize, translate
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Connection parameters
conn_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT') or 5422
}

# Connect to the PostgreSQL server
conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()


def query(sql):
    try:

        # Execute a query
        cursor.execute(sql)
        records = cursor.fetchall()
        return records

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     # Close the cursor and connection
    #     if cursor:
    #         cursor.close()
    #     if conn:
    #         conn.close()


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


@app.route("/api/semantic-search", methods=['POST'])
def api_semantic_search():
    inputs = request.get_json()
    text = inputs['text']
    embedding = encode(text)
    table = inputs['table']
    select_column = inputs['select_column']
    target_column = inputs['target_column']
    limit = inputs['limit']

    sql = f"SELECT {select_column} FROM {table} ORDER BY {target_column} <#> '{embedding}' LIMIT {limit}"

    rows = query(sql)

    return jsonify(rows)


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

    POST /api/semantic-search
    {
        "text": "hello world",
        "table" : "comments",
        "select_column" : "id,text",
        "target_column" : "text_vector",
        "limit" : 10
    }

    </pre>
"""
