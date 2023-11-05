from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "test1234",
    "database": "book_store"
}

# Route to display product list
@app.route('/')
def products():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    return render_template('product_list.html', products=products)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)