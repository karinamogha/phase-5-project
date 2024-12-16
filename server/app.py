#!/usr/bin/env python3

# Standard library imports
import os

# Remote library imports
from flask import request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

# Local imports
from config import app, db
from models import User, Invoice, Memo

# Flask-Migrate setup
migrate = Migrate(app, db)

# JWT setup
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  # Use env var or fallback
jwt = JWTManager(app)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Views and Routes

@app.route('/')
def index():
    return '<h1>Welcome to Orna Cloud API</h1>'

# Authentication routes
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not all(key in data for key in ('name', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred during registration', 'details': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        token = create_access_token(identity=user.id)
        return jsonify({'token': token, 'user_id': user.id}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred during login', 'details': str(e)}), 500

# Invoice routes
@app.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    try:
        data = request.json
        user_id = get_jwt_identity()
        if not all(key in data for key in ('receiver_id', 'amount', 'description')):
            return jsonify({'error': 'Missing required fields'}), 400

        invoice = Invoice(
            sender_id=user_id,
            receiver_id=data['receiver_id'],
            amount=data['amount'],
            description=data['description']
        )
        db.session.add(invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while creating the invoice', 'details': str(e)}), 500


@app.route('/invoices/<int:user_id>', methods=['GET'])
@jwt_required()
def get_invoices(user_id):
    try:
        invoices_sent = Invoice.query.filter_by(sender_id=user_id).all()
        invoices_received = Invoice.query.filter_by(receiver_id=user_id).all()
        return jsonify({
            'invoices_sent': [i.to_dict() for i in invoices_sent],
            'invoices_received': [i.to_dict() for i in invoices_received],
        }), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching invoices', 'details': str(e)}), 500

# Memo routes
@app.route('/memos', methods=['POST'])
@jwt_required()
def create_memo():
    try:
        data = request.json
        user_id = get_jwt_identity()
        if not all(key in data for key in ('receiver_id', 'content')):
            return jsonify({'error': 'Missing required fields'}), 400

        memo = Memo(
            sender_id=user_id,
            receiver_id=data['receiver_id'],
            content=data['content']
        )
        db.session.add(memo)
        db.session.commit()
        return jsonify({'message': 'Memo created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while creating the memo', 'details': str(e)}), 500


@app.route('/memos/<int:user_id>', methods=['GET'])
@jwt_required()
def get_memos(user_id):
    try:
        memos_sent = Memo.query.filter_by(sender_id=user_id).all()
        memos_received = Memo.query.filter_by(receiver_id=user_id).all()
        return jsonify({
            'memos_sent': [m.to_dict() for m in memos_sent],
            'memos_received': [m.to_dict() for m in memos_received],
        }), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching memos', 'details': str(e)}), 500

# Error handling for invalid routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Route not found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)




