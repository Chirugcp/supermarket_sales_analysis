from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Ensure the DATABASE_URL is correctly set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://supermarket_sales_db_user:Vrsr0jKVl0fMaHi38z0ogBOIXJrSe7pc@dpg-cv5k7dlumphs739kq170-a.oregon-postgres.render.com/supermarket_sales_db")

# Function to connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# Root route for testing
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Supermarket Sales API!"})

# Route to test database connection
@app.route('/db_test', methods=['GET'])
def db_test():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")  # Simple query to check DB connection
        cursor.close()
        conn.close()
        return jsonify({"message": "Database connection successful!"})
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to fetch sales data
@app.route('/sales', methods=['GET'])
def get_sales():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM supermarket_sales LIMIT 10;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

