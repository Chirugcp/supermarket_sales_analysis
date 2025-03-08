from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://supermarket_sales_db_user:Vrsr0jKVl0fMaHi38z0ogBOIXJrSe7pc@dpg-cv5k7dlumphs739kq170-a.oregon-postgres.render.com/supermarket_sales_db")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Supermarket Sales API!"})

def get_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM supermarket_sales LIMIT 10;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
