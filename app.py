from flask import Flask
import pymysql
import os 

app = Flask(__name__)

DB_HOST = os.getenv("mydb.cfk0g0esw3n9.eu-north-1.rds.amazonaws.com")
DB_USER = os.getenv("admin")
DB_PASSWORD = os.getenv("Ligmaballs:123")
DB_NAME = os.getenv("mydb")

@app.route("/tables")
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





@app.route('/')
def index():
    return "Flask CI/CD working from ECS! Test??"

@app.route('/stress')
def stress():
    while True: pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
