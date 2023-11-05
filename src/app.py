from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

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
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    return render_template('product_list.html', products=products)


@app.route('/manage_product/<int:product_id>', methods=['GET', 'POST'])
def manage_product(product_id):
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']

        if product_id == 0:
            cursor.execute("INSERT INTO products (title, author, price) VALUES (%s, %s, %s)", (title, author, price))
        else:
            cursor.execute("UPDATE products SET title=%s, author=%s, price=%s WHERE id=%s", (title, author, price, product_id))

        connection.commit()
        cursor.close()
        return redirect('/')

    if product_id == 0:
        return render_template('manage_product.html', product=None)
    else:
        cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        product = cursor.fetchone()
        cursor.close()
        return render_template('manage_product.html', product=product)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']

        cursor.execute("UPDATE products SET title=%s, author=%s, price=%s WHERE id=%s", (title, author, price, product_id))
        connection.commit()
        cursor.close()
        return redirect('/')

    cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
    connection.commit()
    cursor.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)