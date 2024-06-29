from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tree_listings')
def tree_listings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trees WHERE customer = 0")
    trees = cursor.fetchall()
    conn.close()
    return render_template('tree_listings.html', trees=trees)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin_portal', methods=['GET', 'POST'])
def admin_portal():
    if request.method == 'POST':
        action = request.form.get('action')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if action == 'add':
            cursor.execute("INSERT INTO Trees (farmer_name, location, cptpm, trees_available,rental_period) VALUES (?, ?, ?, ?,?)",
                           (request.form['farmer_name'], request.form['location'], request.form['cptpm'], request.form['trees_available'], request.form['rental_period']))
        elif action == 'update':
            cursor.execute("UPDATE Trees SET farmer_name = ?, location = ?, cptpm = ?, trees_available = ?,rental_period = ?,customer = ? WHERE id = ?",
                           (request.form['farmer_name'], request.form['location'], request.form['cptpm'], request.form['trees_available'],request.form['rental_period'],request.form['customer'], request.form['id']))
        elif action == 'delete':
            cursor.execute("DELETE FROM Trees WHERE id = ?", (request.form['id'],))
        
        conn.commit()
        conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trees")
    trees = cursor.fetchall()
    conn.close()
    return render_template('admin_portal.html', trees=trees)

# Database initialization
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Trees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            location TEXT NOT NULL,
            cptpm TEXT NOT NULL,
            trees_available INTEGER NOT NULL,
            rental_period TEXT NOT NULL   ,     
            customer TEXT NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
