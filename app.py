from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

ADMIN_USERNAME = "Deepika"
ADMIN_PASSWORD = "1709"

# DB connection
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Create table
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id SERIAL PRIMARY KEY,
            name TEXT,
            complaint TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/')
        else:
            return "Invalid Login"
    return render_template("login.html")

# Home
@app.route('/')
def home():
    if not session.get('admin'):
        return redirect('/login')
    return render_template("index.html")

# Add complaint
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    complaint = request.form['complaint']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO complaints (name, complaint) VALUES (%s, %s)", (name, complaint))
    conn.commit()
    conn.close()

    return redirect('/')

# View complaints
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM complaints")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", complaints=data)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run()
