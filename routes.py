from flask import Blueprint, request, render_template, g, redirect, url_for, flash
import sqlite3

 
bp = Blueprint('main', __name__)


DATABASE = 'employee.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.row_factory = sqlite3.Row

    return g.db

@bp.teardown_app_request
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@bp.route('/')
@bp.route('/show_table_data')
def show_table_data():
    db = get_db()
    cursor = db.cursor()
    
    employees = cursor.execute("SELECT id, name, age, role FROM employee").fetchall()
    return render_template('index.html', employees=employees)

#add the no duplications here
@bp.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    age = request.form['age']
    role = request.form['role']
    
    db = get_db()
    cursor = db.cursor()
    
    existing_user = cursor.execute("SELECT * FROM employee WHERE name = ? AND age = ? AND role = ?", (name, age, role)).fetchall()
    if existing_user:
        flash('Entry already exists', 'danger')
        return redirect(url_for('main.show_table_data'))
    else:
        db.execute("INSERT INTO employee (name, age, role) VALUES (?, ?, ?)", (name, age, role))
        db.commit()
        flash('Entry added successfully', 'success')
    
    return redirect(url_for('main.show_table_data'))
    


   

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employee WHERE id = ?", (id,))
        employee = cursor.fetchone()
        if employee:
            return render_template('update.html', employee = employee)
        else:
            return "item not found", 404
        
    elif request.method == 'POST':
        update_name = request.form['name']
        update_role = request.form['role']
        update_age = request.form['age']
        
        
        cursor.execute("UPDATE employee SET name = ?, role = ?, age = ? WHERE id = ?", (update_name, update_role, update_age, id))
        db.commit()
        return redirect(url_for('main.show_table_data'))
    
@bp.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("DELETE FROM employee WHERE id = ?", (id,))
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
    finally:
        return redirect(url_for('main.show_table_data'))
