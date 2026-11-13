import sqlite3
import smtplib
import random
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- НАСТРОЙКИ ТВОЕЙ ПОЧТЫ ДЛЯ ОТПРАВКИ КОДОВ ---
SMTP_EMAIL = "SMPT_EMAIL"
SMTP_PASSWORD = "SMPT_PASSWORD"
# ------------------------------------------------

# Временное хранилище кодов подтверждения: {email: code}
verification_codes = {}

# Инициализация базы данных SQLite
def init_db():
    conn = sqlite3.connect("messenger.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 1. Отправка кода подтверждения на реальную почту
@app.route("/send_code", methods=["POST"])
def send_code():
    data = request.json
    email = data.get("email", "").strip()

    conn = sqlite3.connect("messenger.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status": "error", "message": "Эта почта уже зарегистрирована!"}), 400
    conn.close()

    code = str(random.randint(1000, 9999))
    verification_codes[email] = code

    try:
        msg = EmailMessage()
        msg.set_content(f"Твой код подтверждения для регистрации в мессенджере: {code}")
        msg["Subject"] = "Код подтверждения регистрации"
        msg["From"] = SMTP_EMAIL
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)

        return jsonify({"status": "ok", "message": "Код отправлен на почту!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Не удалось отправить письмо. Проверь почту! ({e})"}), 400

# 2. Проверка кода и завершение регистрации
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    code = data.get("code", "").strip()

    if verification_codes.get(email) != code:
        return jsonify({"status": "error", "message": "Неверный код подтверждения!"}), 400

    conn = sqlite3.connect("messenger.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

    del verification_codes[email]
    return jsonify({"status": "ok", "message": "Аккаунт создан!"})

# 3. Вход в аккаунт
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    conn = sqlite3.connect("messenger.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if row and row[0] == password:
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "message": "Неверная почта или пароль!"}), 401

# 4. Отправка и получение сообщений
@app.route("/messages", methods=["GET", "POST"])
def handle_messages():
    conn = sqlite3.connect("messenger.db")
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json
        sender = data.get("sender")
        text = data.get("text")
        cursor.execute("INSERT INTO messages (sender, text) VALUES (?, ?)", (sender, text))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok"})

    cursor.execute("SELECT sender, text FROM messages ORDER BY id ASC")
    msgs = [{"sender": r[0], "text": r[1]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(msgs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)