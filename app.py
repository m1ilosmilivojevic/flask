from flask import Flask, request, render_template
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mydb.cfk0g0esw3n9.eu-north-1.rds.amazonaws.com")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Ligmaballs:123")
DB_NAME = os.getenv("DB_NAME", "mydb")

@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    message = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()
            connection.close()
            message = "User added successfully!"
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template("input_users.html", message=message)

@app.route("/")
def index():
    return render_template("index.html") 




@app.route('/users/health')
def health():
    print(f"Connecting to: host={DB_HOST}, user={DB_USER}, db={DB_NAME}")
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        connection.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/users/tables')
def list_tables():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
        connection.close()
        return f"Tables: {tables}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/users')
def users_index():
    return "Flask CI/CD working from ECS! Under /users"

@app.route('/users/show_all')
def show_all_users():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
        connection.close()
        return f"Users: {users}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/users/stress')
def stress():
    while True: pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
