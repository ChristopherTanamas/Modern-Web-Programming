from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from database import *

@app.before_request
def init_categories():
    categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Groceries']
    for category_name in categories:
        if not Category.query.filter_by(name=category_name).first():
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
    print("Categories initialized")



# API Endpoint: Register User
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"message": "All fields are required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "The Username is already taken"}), 400
        

    hashed_password = generate_password_hash(password)

    try:
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 400

    return jsonify({"message": "Login successful"}), 200


# API Endpoint: Add Category
@app.route('/api/category', methods=['POST'])
def add_category():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"message": "Category name is required"}), 400

    try:
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    date = data.get('date')
    amount = data.get('amount')
    description = data.get('description')
    category_id = data.get('category_id')  # Ini yang Anda kirimkan dari Vue.js

    # Pastikan semua data sudah ada
    if not all([date, amount, category_id]):
        return jsonify({"message": "All fields are required"}), 400

    # Jika description kosong, set null
    if description == "" or description is None:
        description = None

    # Validasi kategori
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404

    try:
        # Menyimpan transaksi baru
        new_transaction = Transaction(
            date=date, amount=amount, description=description, category_id=category_id
        )
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({"message": "Transaction added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500



# API Endpoint: Get Categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'visible': category.visible,
                'transactions': [{'date': t.date, 'amount': t.amount, 'description': t.description} for t in category.transactions]
            })
        return jsonify(categories_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/workspace', methods=['GET'])
def get_spending():
    try:
        # Ambil semua transaksi dari database
        transactions = Transaction.query.all()
        
        # Buat data transaksi untuk dikirim sebagai respons
        spending_data = [
            {
                'transid': transaction.id,
                'category': transaction.category.name,  # Pastikan relasi kategori sudah benar
                'amount': transaction.amount,
                'date': transaction.date,
                'description': transaction.description
            }
            for transaction in transactions
        ]
        
        return jsonify({"status": "success", "spending": spending_data}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/category/<int:category_id>/limit', methods=['PUT'])
def update_category_limit(category_id):
    data = request.json
    new_limit = data.get('limit')

    if new_limit is None or not isinstance(new_limit, int):
        return jsonify({"message": "Valid limit value is required"}), 400

    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        category.limit = new_limit
        db.session.commit()
        return jsonify({"message": "Category limit updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# API Endpoint: Delete Transaction
@app.route('/api/deletetransaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"message": "Transaction not found"}), 404

        db.session.delete(transaction)
        db.session.commit()

        return jsonify({"message": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route('/api/updatetransaction/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    try:
        # Mencari transaksi berdasarkan ID
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return jsonify({"message": "Transaction not found"}), 404

        # Mengambil data yang dikirimkan dari frontend
        data = request.json

        # Memperbarui field transaksi sesuai data yang diterima
        transaction.date = data.get('date', transaction.date)
        transaction.amount = data.get('amount', transaction.amount)
        transaction.description = data.get('description', transaction.description)
        transaction.category_id = data.get('category_id', transaction.category_id)

        # Menyimpan perubahan ke database
        db.session.commit()

        return jsonify({"message": "success"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback jika ada error
        return jsonify({"message": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
