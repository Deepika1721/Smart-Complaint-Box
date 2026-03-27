from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"

ADMIN_USERNAME = "Deepika"
ADMIN_PASSWORD = "1709"

def init_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/')
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route('/')
def home():
    if not session.get('admin'):
        return redirect('/login')

    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    data = c.fetchall()
    conn.close()
    return render_template("index.html", complaints=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    complaint = request.form['complaint']

    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO complaints (name, complaint) VALUES (?, ?)", (name, complaint))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
