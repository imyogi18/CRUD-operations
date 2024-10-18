from flask import Flask, request, redirect, url_for, render_template, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

db_config = {
    'user': 'root',
    'password': '94Gry610@',
    'host': '127.0.0.1',
    'database': 'student_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return redirect(url_for('view_students'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        dob = request.form.get('dob')
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO student (name, email, age, dob, phone_no, address) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, email, age, dob, phone_no, address)
            )
            conn.commit()
            flash('Student registered successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('view_students'))
    return render_template('register.html')

@app.route('/student')
def view_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM student')
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        dob = request.form.get('dob')
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        
        try:
            cursor.execute(
                'UPDATE student SET name=%s, email=%s, age=%s, dob=%s, phone_no=%s, address=%s WHERE id=%s',
                (name, email, age, dob, phone_no, address, id)
            )
            conn.commit()
            flash('Student updated successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('view_students'))
    cursor.execute('SELECT * FROM student WHERE id=%s', (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM student WHERE id=%s', (id,))
        conn.commit()
        flash('Student deleted successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(debug=True)
