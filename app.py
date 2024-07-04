import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    
    db = get_db()
    db.execute('INSERT INTO contacts (name, surname, phone) VALUES (?, ?, ?)', (name, surname, phone))
    db.commit()
    
    return "Form submitted!"

@app.route('/contacts')
def contacts():
    db = get_db()
    cur = db.execute('SELECT id, name, surname, phone FROM contacts')
    entries = cur.fetchall()
    return render_template('contacts.html', entries=entries)

@app.route('/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    db = get_db()
    db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    db.commit()
    return redirect(url_for('contacts'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
