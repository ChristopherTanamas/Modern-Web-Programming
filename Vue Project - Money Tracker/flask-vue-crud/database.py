from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moneytracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Model Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    visible = db.Column(db.Boolean, default=True)
    limit = db.Column(db.Integer, default=100000)
    transactions = db.relationship('Transaction', backref='category', lazy=True)

# Model Transaction
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True, default="")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
