from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

ADMIN_USERNAME = "Deepika"
ADMIN_PASSWORD = "1709"

# PostgreSQL URL from Render environment
DATABASE_URL = os.environ.get("DATABASE_URL")


# DB connection
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


# USER HOME PAGE (complaint form)
@app.route('/')
def home():
    return render_template("index.html")


# ADD COMPLAINT
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


# ADMIN LOGIN
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid Login"

    return render_template("login.html")


# ADMIN DASHBOARD
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin-login')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM complaints ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", complaints=data)


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin-login')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
