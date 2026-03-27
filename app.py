from flask import Flask, render_template, request, redirect, session
import sqlite3
import datetime
import os

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USERNAME = "Deepika"
ADMIN_PASSWORD = "1709"

DB_PATH = "complaints.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT,
            status TEXT DEFAULT 'Pending',
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    complaint = request.form['complaint']

    if not name or not complaint:
        return "Please fill all fields"

    date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints (name, complaint, date) VALUES (?, ?, ?)",
                   (name, complaint, date))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return render_template('admin.html', error="Invalid Username or Password")
    return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/admin')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    count = cursor.fetchone()[0]

    conn.close()

    return render_template('dashboard.html', data=data, count=count)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE name LIKE ? OR complaint LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%'))
    data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    count = cursor.fetchone()[0]

    conn.close()

    return render_template('dashboard.html', data=data, count=count)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    status = request.form['status']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM complaints WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)