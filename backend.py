from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, WithJsonSchema
from fn import encode, summarize, translate
from dotenv import load_dotenv
from typing import List, Annotated
import psycopg2
import os
import json

load_dotenv()


app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connection parameters
conn_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT') or 5422
}

try:
    # Trycatch Connect to the PostgreSQL server
    conn = psycopg2.connect(**conn_params)
    print("Connection to PostgreSQL server established successfully.")
    cursor = conn.cursor()

    def query(sql):
        try:
            # Execute a query
            cursor.execute(sql)
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="Database query error")

    class SemanticBody(BaseModel):
        text: str
        table: str
        retrieved_columns: str
        target_column: str
        limit: int

    @app.post("/api/semantic-search", name="Semantic Search", description="This endpoint takes a text as input and returns a list of rows from a table that match the text. The retrieved columns are the columns that you want to retrieve from the table separated by comma. The target column is the column in the database that has the type of `vector`.")
    async def api_semantic_search(inputs: SemanticBody):
        text = inputs.text
        embedding = encode(text)
        table = inputs.table
        select_column = inputs.retrieved_columns
        target_column = inputs.target_column
        limit = inputs.limit

        sql = f"SELECT {select_column} FROM {table} ORDER BY {target_column} <#> '{embedding}' LIMIT {limit}"

        rows = query(sql)

        return JSONResponse(content=rows)

except Exception as e:
    print(f"Error connecting to PostgreSQL server: {e}")


# Sample data
data = {
    "hello": "world",
    "man": [
        "aaa", "bbb", "ccc"
    ]
}


class VectorizeBody(BaseModel):
    text: str


@app.post(
    "/api/vectorize",
    description="This endpoint takes a text as input and returns a vectorized representation of it. The Vector size is 1024.", name="Text to Vector",
    response_model=List[float],

)
async def api_vectorize(inputs: VectorizeBody = Body(..., example={"text": "Hello, world!"})):
    vec = encode(inputs.text)
    return JSONResponse(content=json.loads(vec))


class SummarizeBody(BaseModel):
    text: str


@app.post("/api/summarize", name="Summarize Text", description="This endpoint takes a text as input and returns a summary of it.")
async def api_summarize(inputs: SummarizeBody):
    summary = summarize(inputs.text)
    return JSONResponse(content=summary)


class TranslateBody(BaseModel):
    text: str
    target_language: str


@app.post("/api/translate", name="Translate Text", description="This endpoint takes a text as input and returns a translated text in the specified language.")
async def api_translate(inputs: TranslateBody):
    lang = inputs.target_language
    translation = translate(inputs.text, lang=lang)
    return JSONResponse(content=translation)


@app.get("/")
async def get_index():
    return HTMLResponse("""
      <html>
      <head>
          <title>NLP API</title>
      </head>
      <body>
          <h1>NLP API</h1>
          <p>This is a simple NLP API that uses FastAPI and PostgreSQL.</p>
          <p>You can use it to vectorize text, summarize text, translate text, and perform semantic search.</p>
          <p>Refer to the <a href="/docs">API documentation</a> for more information.</p>
      </body>
      </html>
""")
