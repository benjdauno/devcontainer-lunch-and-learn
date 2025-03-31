import os
import time
from flask import Flask, render_template, jsonify
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

def get_db_connection():
    # Get database connection details from environment variables
    db_config = {
        'host': os.environ.get('DB_HOST', 'proxysql'),
        'port': int(os.environ.get('DB_PORT', 6033)),
        'user': os.environ.get('DB_USER', 'myuser'),
        'password': os.environ.get('DB_PASSWORD', 'mypassword'),
        'database': os.environ.get('DB_NAME', 'mydb'),
        'cursorclass': DictCursor
    }
    
    # Try to establish a connection with retries
    max_retries = 10
    retry_interval = 3
    
    for i in range(max_retries):
        try:
            connection = pymysql.connect(**db_config)
            return connection
        except pymysql.Error as e:
            if i < max_retries - 1:
                print(f"Database connection failed. Retrying in {retry_interval} seconds... ({e})")
                time.sleep(retry_interval)
            else:
                raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/db-test')
def db_test():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Create a table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            
            # Insert a test row
            cursor.execute("INSERT INTO test_table (name) VALUES (%s)", ("Test entry",))
            conn.commit()
            
            # Query all rows
            cursor.execute("SELECT * FROM test_table ORDER BY created_at DESC LIMIT 10")
            results = cursor.fetchall()
        
        conn.close()
        return jsonify({"status": "success", "data": results})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
