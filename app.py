from flask import Flask, request, render_template, jsonify
import pymysql
import os
from dotenv import load_dotenv

# Load .env once
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

app = Flask(__name__)

# DB config
DB_HOST = os.getenv("DB_HOST", "mydb.cfk0g0esw3n9.eu-north-1.rds.amazonaws.com")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Ligmaballs:123")
DB_NAME = os.getenv("DB_NAME", "mydb")

# Helper to connect
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/")
def index():
    return "Welcome to the Users API!"

@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    message = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()
            connection.close()
            message = "User added successfully!"
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template("input_users.html", message=message)

@app.route("/users/creds")
def credentials():
    return f"DB_HOST: {DB_HOST}, DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}, DB_NAME: {DB_NAME}"

@app.route('/users/health')
def health():
    try:
        connection = get_db_connection()
        connection.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/users/tables')
def list_tables():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
        connection.close()
        return jsonify(tables)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/users')
def users_index():
    return "Flask CI/CD working from ECS! Under /users"

@app.route('/users/show_all')
def show_all_users():
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
        connection.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/users/stress')
def stress():
    timeout = 5
    start = time.time()
    while time.time() - start < timeout:
        pass
    return "Stress test complete!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
