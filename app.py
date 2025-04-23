from flask import Flask, request, render_template_string
import pymysql
import os 

app = Flask(__name__)


DB_HOST = os.getenv("database-1.cluster-cfk0g0esw3n9.eu-north-1.rds.amazonaws.com")
DB_USER = os.getenv("admin")
DB_NAME = os.getenv("database-1")
DB_PASSWORD = os.getenv("")

@app.route("/tables")
def list_tables():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
        connection.close()
        return f"Tables: {tables}"
    except Exception as e:
        return f"Error: {str(e)}"

# HTML template
form_html = """
<!doctype html>
<title>User Form</title>
<h2>Add a user</h2>
<form method=post>
  <input type=text name=username required>
  <input type=submit value=Add>
</form>
<p>{{ message }}</p>
"""

@app.route('/users', methods=['GET', 'POST'])
def users():
    message = ""
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        with conn.cursor() as cursor:
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE
                );
            """)
            conn.commit()

            if request.method == 'POST':
                username = request.form['username']
                try:
                    cursor.execute("INSERT INTO users (username) VALUES (%s);", (username,))
                    conn.commit()
                    message = f"User '{username}' added successfully."
                except pymysql.err.IntegrityError:
                    message = f"User '{username}' already exists."

        conn.close()
    except Exception as e:
        message = f"Error: {e}"

    return render_template_string(form_html, message=message)



@app.route('/')
def index():
    return "Flask CI/CD working from ECS! Test??"

@app.route('/stress')
def stress():
    while True: pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
