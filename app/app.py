from flask import Flask
import os
import psycopg2
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "testdb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")
db_alert_sent = False

def send_discord(message):
    if not DISCORD_WEBHOOK_URL:
        return

    try:
        requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=5
        )
    except Exception as e:
        print(f"Discord notify failed: {e}")

@app.route("/health")
def health():
    global db_alert_sent
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()

        if db_alert_sent:
            send_discord(
                "🚀 にゃん.jp DB接続復旧\nDatabase connection restored."
            )
            db_alert_sent = False

        db_status = "OK"

    except Exception as e:
        print(f"[HEALTH CHECK ERROR] Database connection failed: {e}", flush=True)

        if not db_alert_sent:
            send_discord(
                f"🚨 にゃん.jp DB接続エラー\n{e}"
            )
            db_alert_sent = True

        db_status = "NG"

    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="UTF-8">
      <title>Health Check | にゃん.jp</title>
      <style>
        body {{
          margin: 0;
          background: #0f1115;
          color: #f5f5f5;
          font-family: system-ui, sans-serif;
          line-height: 1.7;
        }}
        .container {{
          max-width: 900px;
          margin: 0 auto;
          padding: 64px 24px;
        }}
        a {{
          color: #4ade80;
          text-decoration: none;
          font-weight: bold;
        }}
        h1 {{
          font-size: 52px;
          margin: 32px 0 12px;
        }}
        .card {{
          background: #181b22;
          border: 1px solid #2a2f3a;
          border-radius: 20px;
          padding: 28px;
          box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }}
        .ok {{
          color: #4ade80;
          font-weight: bold;
        }}
        .ng {{
          color: #f87171;
          font-weight: bold;
        }}
      </style>
    </head>
    <body>
      <main class="container">
        <a href="/">← Back to Top</a>

        <h1>Health Check</h1>

        <div class="card">
          <h2>System Status</h2>
          <p><strong>Server:</strong> <span class="ok">OK</span></p>
          <p><strong>Database:</strong> <span class="{'ok' if db_status == 'OK' else 'ng'}">{db_status}</span></p>
          <p><strong>Check:</strong> Database Connection Verified</p>
        </div>
      </main>
    </body>
    </html>
    """

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/")
def home():
    return "Application server is running. Database connection route is available."

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
    cur.execute("INSERT INTO test (msg) VALUES ('DB health check: PostgreSQL connection OK');")
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

    messages = "<br>".join([r[0] for r in rows]) or "no data"

    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="UTF-8">
      <title>Database Status | にゃん.jp</title>
      <style>
        body {{
          margin: 0;
          background: #0f1115;
          color: #f5f5f5;
          font-family: system-ui, sans-serif;
          line-height: 1.7;
        }}

        .container {{
          max-width: 900px;
          margin: 0 auto;
          padding: 64px 24px;
        }}

        a {{
          color: #4ade80;
          text-decoration: none;
          font-weight: bold;
        }}

        h1 {{
          font-size: 52px;
          margin: 32px 0 12px;
        }}

        .card {{
          background: #181b22;
          border: 1px solid #2a2f3a;
          border-radius: 20px;
          padding: 28px;
          box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }}

        .ok {{
          color: #4ade80;
          font-weight: bold;
        }}

        .response {{
          margin-top: 16px;
          padding: 16px;
          background: #0f1115;
          border-radius: 12px;
          border: 1px solid #2a2f3a;
          color: #c7c7c7;
        }}
      </style>
    </head>
    <body>
      <main class="container">
        <a href="/">← Back to Top</a>

        <h1>Database Status</h1>

        <div class="card">
          <h2>✅ PostgreSQL Connected</h2>
          <p><strong>Status:</strong> <span class="ok">Connected</span></p>
          <p><strong>Engine:</strong> PostgreSQL</p>
          <p><strong>Query:</strong> SELECT msg FROM test;</p>

          <div class="response">
            <strong>Response from DB:</strong><br>
            {messages}
          </div>
        </div>
      </main>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

