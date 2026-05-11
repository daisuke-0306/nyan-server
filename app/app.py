from flask import Flask
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "testdb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/")
def home():
    return "App + DB connected!"

@app.route("/init")
def init():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, msg TEXT);")
    conn.commit()
    cur.close()
    conn.close()
    return "table created"

@app.route("/save")
def save():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO test (msg) VALUES ('hello from db');")
    conn.commit()
    cur.close()
    conn.close()
    return "saved"

@app.route("/read")
def read():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT msg FROM test;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return "<br>".join([r[0] for r in rows]) or "no data"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

