from flask import Flask
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask CI/CD working from ECS!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
