from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL Connection URL (Update with your actual details)
DATABASE_URL = "postgresql://supermarket_sales_db_user:Vrsr0jKVl0fMaHi38z0ogBOIXJrSe7pc@dpg-cv5k7dlumphs739kq170-a.oregon-postgres.render.com/supermarket_sales_db"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Supermarket Sales API!"})

@app.route('/sales', methods=['GET'])
def get_sales():
    """Fetch 10 rows from the supermarket_sales table and convert TIME fields to strings."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch data
        cursor.execute("SELECT * FROM supermarket_sales LIMIT 10;")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows into a list of dictionaries
        results = []
        for row in rows:
            row_dict = dict(zip(column_names, row))

            # Convert TIME and DATE fields to string format
            for key, value in row_dict.items():
                if isinstance(value, (bytes, memoryview)):  # Handle binary data
                    row_dict[key] = value.decode("utf-8")
                elif isinstance(value, (str, int, float)):  # Keep normal values
                    continue
                else:  # Convert Date and Time fields
                    row_dict[key] = str(value)

            results.append(row_dict)

        cursor.close()
        conn.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


