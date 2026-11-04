import os
import pymysql
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

def require_api_key():
    expected_key = os.environ.get("API_KEY")
    provided_key = request.headers.get("X-API-Key")

    if not expected_key or provided_key != expected_key:
        abort(401)

def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="flask_user",
        password=os.environ["DB_PASSWORD"],
        database="three_tier_db",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return """
    <h1>Three-Tier Flask Application</h1>
    <p>Application is running on AWS EC2!</p>
    <p><a href="/users">View Users (API key required)</a></p>
    """

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/users")
def users():
    require_api_key()
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
        return jsonify(results)
    finally:
        connection.close()
