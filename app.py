from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from config import config

""" models: """
from models.ModelUser import ModelUser

""" entities: """
from models.entities.User import User

app = Flask(__name__)

db = MySQL(app)

""" settings """
app.secret_key = 'mysecretkey'

""" ruta raiz """
@app.route('/')
def index():
    return redirect(url_for('login'))

""" Login """
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(0, username, password)
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if User.check_password(logged_user.password, user.password):
                return redirect(url_for('task_page'))
            else:
                flash('Usuario o contraseña incorrectos')
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('auth/login.html')


""" registro """
@app.route('/register')
def register():
    return render_template('auth/register.html')

""" Metodo post """
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        hashed_password = User.hash_password(password)
        cur = db.connection.cursor()
        cur.execute('INSERT INTO user (username, password, fullname) VALUES (%s, %s, %s)', (username, hashed_password, fullname))
        db.connection.commit()
        flash('Se registró correctamente')
        return redirect(url_for('login'))

""" To-Do List Routes """
@app.route('/add_task', methods=['GET'])
def add_task_page():
    return render_template('add_task.html')

""" metodo post """
@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cur = db.connection.cursor()
        cur.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (name, description))
        db.connection.commit()
        return redirect(url_for('add_task_page'))

@app.route('/tasks/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    completed = request.form['completed']
    cur = db.connection.cursor()
    cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))
    db.connection.commit()
    return redirect(url_for('task_page'))

@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.connection.commit()
    return redirect(url_for('task_page'))

@app.route('/tasks/assign/<int:task_id>', methods=['POST'])
def assign_resources(task_id):
    resource_ids = request.form.getlist('resource_ids')
    cur = db.connection.cursor()
    for resource_id in resource_ids:
        cur.execute("INSERT INTO task_resources (task_id, resource_id) VALUES (%s, %s)", (task_id, resource_id))
    db.connection.commit()
    return redirect(url_for('task_page'))

""" direcciona a la lista de tareas """
@app.route('/task_page')
def task_page():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    tasks = [{'id': row[0], 'name': row[1], 'description': row[2], 'completed': bool(row[3])} for row in tasks]
    return render_template('task.html', tasks=tasks)

@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    cur = db.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cur.execute("UPDATE tasks SET name = %s, description = %s WHERE id = %s", (name, description, task_id))
        db.connection.commit()
        return redirect(url_for('task_page'))
    
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    task = {'id': task[0], 'name': task[1], 'description': task[2], 'completed': bool(task[3])}
    return render_template('edit_task.html', task=task)

""" servidor """
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
