import base64
import hashlib
import hmac
import os
from functools import wraps
import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

def db_config():
    return {"host": os.getenv("DB_HOST", "localhost"), "database": os.getenv("DB_NAME", "todo_app"), "user": os.getenv("DB_USER", "todo_user"), "password": os.getenv("DB_PASSWORD", "todo_password")}

def get_db():
    return mysql.connector.connect(**db_config())

def token_for(user_id):
    value = str(user_id)
    secret = os.getenv("TOKEN_SECRET", "development-secret").encode()
    signature = hmac.new(secret, value.encode(), hashlib.sha256).hexdigest()
    return base64.urlsafe_b64encode(f"{value}:{signature}".encode()).decode()

def user_from_token(token):
    try:
        value, signature = base64.urlsafe_b64decode(token.encode()).decode().split(":", 1)
        secret = os.getenv("TOKEN_SECRET", "development-secret").encode()
        expected = hmac.new(secret, value.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, expected):
            return int(value)
    except (ValueError, TypeError, UnicodeDecodeError):
        pass
    return None

def auth_required(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "authentication required"}), 401
        user_id = user_from_token(header[7:])
        if user_id is None:
            return jsonify({"error": "invalid token"}), 401
        return handler(user_id, *args, **kwargs)
    return wrapped

@app.get("/health")
def health():
    try:
        connection = get_db(); connection.close()
        return jsonify({"status": "ok"})
    except mysql.connector.Error:
        return jsonify({"status": "degraded"}), 503

@app.post("/api/auth/register")
def register():
    body = request.get_json(silent=True) or {}
    username, password = str(body.get("username", "")).strip().lower(), str(body.get("password", ""))
    if len(username) < 3 or len(password) < 4:
        return jsonify({"error": "username must be 3+ characters and password 4+ characters"}), 400
    connection = get_db(); cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, SHA2(%s, 256))", (username, password)); connection.commit(); user_id = cursor.lastrowid
    except mysql.connector.IntegrityError:
        connection.rollback(); return jsonify({"error": "username already exists"}), 409
    finally:
        cursor.close(); connection.close()
    return jsonify({"token": token_for(user_id), "username": username}), 201

@app.post("/api/auth/login")
def login():
    body = request.get_json(silent=True) or {}
    username, password = str(body.get("username", "")).strip().lower(), str(body.get("password", ""))
    connection = get_db(); cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users WHERE username=%s AND password_hash=SHA2(%s, 256)", (username, password)); user = cursor.fetchone()
    cursor.close(); connection.close()
    if not user: return jsonify({"error": "invalid username or password"}), 401
    return jsonify({"token": token_for(user["id"]), "username": user["username"]})

@app.get("/api/todos")
@auth_required
def list_todos(user_id):
    connection = get_db(); cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, title, completed, created_at FROM todos WHERE user_id=%s ORDER BY created_at DESC", (user_id,)); todos = cursor.fetchall()
    cursor.close(); connection.close()
    for todo in todos: todo["completed"], todo["created_at"] = bool(todo["completed"]), todo["created_at"].isoformat()
    return jsonify(todos)

@app.post("/api/todos")
@auth_required
def create_todo(user_id):
    title = str((request.get_json(silent=True) or {}).get("title", "")).strip()
    if not title or len(title) > 200: return jsonify({"error": "title is required and must be 200 characters or fewer"}), 400
    connection = get_db(); cursor = connection.cursor(); cursor.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s)", (user_id, title)); connection.commit(); todo_id = cursor.lastrowid; cursor.close(); connection.close()
    return jsonify({"id": todo_id, "title": title, "completed": False}), 201

@app.patch("/api/todos/<int:todo_id>")
@auth_required
def update_todo(user_id, todo_id):
    body = request.get_json(silent=True) or {}
    if "completed" not in body: return jsonify({"error": "completed is required"}), 400
    connection = get_db(); cursor = connection.cursor(); cursor.execute("UPDATE todos SET completed=%s WHERE id=%s AND user_id=%s", (bool(body["completed"]), todo_id, user_id)); connection.commit(); changed = cursor.rowcount; cursor.close(); connection.close()
    if not changed: return jsonify({"error": "todo not found"}), 404
    return jsonify({"id": todo_id, "completed": bool(body["completed"])})

@app.delete("/api/todos/<int:todo_id>")
@auth_required
def delete_todo(user_id, todo_id):
    connection = get_db(); cursor = connection.cursor(); cursor.execute("DELETE FROM todos WHERE id=%s AND user_id=%s", (todo_id, user_id)); connection.commit(); changed = cursor.rowcount; cursor.close(); connection.close()
    if not changed: return jsonify({"error": "todo not found"}), 404
    return jsonify({"deleted": True})

@app.get("/api/notifications")
@auth_required
def notifications(user_id):
    connection = get_db(); cursor = connection.cursor(dictionary=True); cursor.execute("SELECT message, created_at FROM notifications WHERE user_id=%s ORDER BY created_at DESC LIMIT 20", (user_id,)); rows = cursor.fetchall(); cursor.close(); connection.close()
    for row in rows: row["created_at"] = row["created_at"].isoformat()
    return jsonify(rows)

