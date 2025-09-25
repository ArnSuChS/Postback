from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import sqlite3
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

DB_NAME = "postback_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS postbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            status TEXT,
            instrument_token TEXT,
            filled_quantity REAL,
            average_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT order_id, status, instrument_token, filled_quantity, average_price, timestamp
        FROM postbacks ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows)


@app.route("/kite_postback", methods=["POST"])
def kite_postback():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    order_id = data.get("order_id")
    status = data.get("status")
    instrument_token = str(data.get("instrument_token", ""))
    filled_quantity = data.get("filled_quantity", 0)
    average_price = data.get("average_price", 0.0)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO postbacks (order_id, status, instrument_token, filled_quantity, average_price) "
        "VALUES (?, ?, ?, ?, ?)",
        (order_id, status, instrument_token, filled_quantity, average_price),
    )
    conn.commit()
    conn.close()

    socketio.emit("new_postback", data)

    return jsonify({"message": "Postback received"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
