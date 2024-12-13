from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # Relationships
    invoices_sent = db.relationship('Invoice', backref='sender', foreign_keys='Invoice.sender_id', cascade='all, delete')
    invoices_received = db.relationship('Invoice', backref='receiver', foreign_keys='Invoice.receiver_id', cascade='all, delete')
    memos_sent = db.relationship('Memo', backref='sender', foreign_keys='Memo.sender_id', cascade='all, delete')
    memos_received = db.relationship('Memo', backref='receiver', foreign_keys='Memo.receiver_id', cascade='all, delete')

    # Association proxy (example if you need it)
    sent_invoice_ids = association_proxy('invoices_sent', 'id')
    received_invoice_ids = association_proxy('invoices_received', 'id')


class Invoice(db.Model, SerializerMixin):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Serialized fields
    serialize_rules = ('-sender.invoices_sent', '-receiver.invoices_received')


class Memo(db.Model, SerializerMixin):
    __tablename__ = 'memos'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Serialized fields
    serialize_rules = ('-sender.memos_sent', '-receiver.memos_received')

