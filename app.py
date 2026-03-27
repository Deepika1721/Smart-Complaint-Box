from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database
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

# Home page (show complaints)
@app.route('/')
def home():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    data = c.fetchall()
    conn.close()
    return render_template("index.html", complaints=data)

# Add complaint
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

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
