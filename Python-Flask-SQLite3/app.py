from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
    except Error as e:
        print(e)
    return conn

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT NOT NULL,
                        product_number TEXT NOT NULL,
                        quantity_of_product TEXT NOT NULL)''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', students=data)

@app.route('/productos')
def productos():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('productos.html', products=data)

@app.route('/insert_user', methods=['POST'])
def insert_user():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not name or not email or not phone:
            flash("All fields are required!")
            return redirect(url_for('index'))

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO students (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
            conn.commit()
            flash("Data Inserted Successfully")
        except Error as e:
            flash(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('index'))

@app.route('/delete_user/<int:id_data>', methods=['GET'])
def delete_user(id_data):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (id_data,))
        conn.commit()
        flash("Record Has Been Deleted Successfully")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('index'))

@app.route('/update_user', methods=['POST'])
def update_user():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not id_data or not name or not email or not phone:
            flash("All fields are required!")
            return redirect(url_for('index'))

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE students SET name=?, email=?, phone=?
                WHERE id=?
            """, (name, email, phone, id_data))
            conn.commit()
            flash("Data Updated Successfully")
        except Error as e:
            flash(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('index'))

@app.route('/insert_productos', methods=['POST'])
def insert_productos():
    if request.method == "POST":
        product_name = request.form['product_name']
        product_number = request.form['product_number']
        quantity_of_product = request.form['quantity_of_product']

        if not product_name or not product_number or not quantity_of_product:
            flash("All fields are required!")
            return redirect(url_for('productos'))

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO products (product_name, product_number, quantity_of_product) VALUES (?, ?, ?)", (product_name, product_number, quantity_of_product))
            conn.commit()
            flash("Data Inserted Successfully")
        except Error as e:
            flash(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('productos'))

@app.route('/delete_productos/<int:id_data>', methods=['GET'])
def delete_productos(id_data):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (id_data,))
        conn.commit()
        flash("Record Has Been Deleted Successfully")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('productos'))

@app.route('/update_productos', methods=['POST'])
def update_productos():
    if request.method == 'POST':
        id_data = request.form['id']
        product_name = request.form['product_name']
        product_number = request.form['product_number']
        quantity_of_product = request.form['quantity_of_product']

        if not id_data or not product_name or not product_number or not quantity_of_product:
            flash("All fields are required!")
            return redirect(url_for('productos'))

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE products SET product_name=?, product_number=?, quantity_of_product=?
                WHERE id=?
            """, (product_name, product_number, quantity_of_product, id_data))
            conn.commit()
            flash("Data Updated Successfully")
        except Error as e:
            flash(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('productos'))

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                session['username'] = username
                return redirect(url_for('index'))
    return render_template('login.html')

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
    return render_template('registro.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
