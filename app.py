from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLE
conn = get_db_connection()

conn.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
''')

conn.commit()
conn.close()

# HOME PAGE
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)

# ADD TASK
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()

    return redirect('/')

# DELETE TASK
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db_connection()

    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# EDIT TASK PAGE
@app.route('/edit/<int:id>')
def edit_task(id):
    conn = get_db_connection()

    task = conn.execute(
        'SELECT * FROM tasks WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    return render_template('edit.html', task=task)

# UPDATE TASK
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']

    conn = get_db_connection()

    conn.execute(
        'UPDATE tasks SET title = ? WHERE id = ?',
        (title, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)