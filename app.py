from flask import Flask
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "database-1.cluster-cfk0g0esw3n9.eu-north-1.rds.amazonaws.com")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Ligmaballs:123")
DB_NAME = os.getenv("DB_NAME", "database-1-instance-1")

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

@app.route('/users/stress')
def stress():
    while True: pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
