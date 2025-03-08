from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL Connection URL (Replace with your actual details)
DATABASE_URL = "postgresql://supermarket_sales_db_user:Vrsr0jKVl0fMaHi38z0ogBOIXJrSe7pc@dpg-cv5k7dlumphs739kq170-a.oregon-postgres.render.com/supermarket_sales_db"

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    """Home Route - Basic Health Check"""
    return "Flask app is working!"

@app.route('/sales', methods=['GET'])
def get_sales():
    """Fetch 10 rows from the supermarket_sales table."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM supermarket_sales LIMIT 10;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

