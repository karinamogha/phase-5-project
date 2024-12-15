#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Local imports
from config import app, db, api
from models import User, Invoice, Memo  # Import models

# Flask-Migrate setup
migrate = Migrate(app, db)

# JWT setup
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# Views and Routes

@app.route('/')
def index():
    return '<h1>Welcome to Orna Cloud API</h1>'

# Authentication routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not all(key in data for key in ('name', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or user.password != data['password']:  # Insecure: Use hashed passwords in production
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'token': token, 'user_id': user.id}), 200

# Invoice routes
@app.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
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


@app.route('/invoices/<int:user_id>', methods=['GET'])
@jwt_required()
def get_invoices(user_id):
    invoices_sent = Invoice.query.filter_by(sender_id=user_id).all()
    invoices_received = Invoice.query.filter_by(receiver_id=user_id).all()
    return jsonify({
        'invoices_sent': [i.to_dict() for i in invoices_sent],
        'invoices_received': [i.to_dict() for i in invoices_received],
    }), 200

# Memo routes
@app.route('/memos', methods=['POST'])
@jwt_required()
def create_memo():
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


@app.route('/memos/<int:user_id>', methods=['GET'])
@jwt_required()
def get_memos(user_id):
    memos_sent = Memo.query.filter_by(sender_id=user_id).all()
    memos_received = Memo.query.filter_by(receiver_id=user_id).all()
    return jsonify({
        'memos_sent': [m.to_dict() for m in memos_sent],
        'memos_received': [m.to_dict() for m in memos_received],
    }), 200

# Error handling for invalid routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Route not found'}), 404

if __name__ == '__main__':
    app.run(port=3000, debug=True)



