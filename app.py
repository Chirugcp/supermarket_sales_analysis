from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL Connection URL (Update with your actual details)
DATABASE_URL = "postgresql://supermarket_sales_db_user:Vrsr0jKVl0fMaHi38z0ogBOIXJrSe7pc@dpg-cv5k7dlumphs739kq170-a.oregon-postgres.render.com/supermarket_sales_db"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/sales', methods=['GET'])
def get_sales():
    """Fetch 10 rows from the supermarket_sales table and convert time fields to strings."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch data
        cursor.execute("SELECT * FROM supermarket_sales LIMIT 10;")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Convert results into a list of dictionaries
        results = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            
            # Convert TIME and DATE objects to strings
            if "Time" in row_dict and isinstance(row_dict["Time"], (str, bytes)) is False:
                row_dict["Time"] = row_dict["Time"].strftime("%H:%M:%S")

            if "Date" in row_dict and isinstance(row_dict["Date"], (str, bytes)) is False:
                row_dict["Date"] = row_dict["Date"].strftime("%Y-%m-%d")

            results.append(row_dict)

        cursor.close()
        conn.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


