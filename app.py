# app.py
from flask import Flask, request, render_template, jsonify
import pymysql
import time
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# DB Connection helper
def get_db_connection():
    return pymysql.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
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
    return f"DB_HOST: {app.config['DB_HOST']}, DB_USER: {app.config['DB_USER']}, DB_PASSWORD: {app.config['DB_PASSWORD']}, DB_NAME: {app.config['DB_NAME']}"

@app.route("/users/health")
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
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
