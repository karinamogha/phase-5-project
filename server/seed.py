#!/usr/bin/env python3

# Standard library imports
from random import choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Invoice, Memo

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Clear existing data
        db.session.query(Memo).delete()
        db.session.query(Invoice).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Create Users
        users = []
        for _ in range(5):
            user = User(
                name=fake.name(),
                email=fake.email(),
                password="password"  # Simplified for seeding; use hashed passwords in production
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

        # Create Invoices
        invoices = []
        for _ in range(10):
            sender = rc(users)
            receiver = rc([u for u in users if u != sender])  # Avoid self-sending invoices
            invoice = Invoice(
                sender_id=sender.id,
                receiver_id=receiver.id,
                amount=round(fake.random_number(digits=4), 2),  # Random amount
                description=fake.sentence()
            )
            invoices.append(invoice)
        db.session.add_all(invoices)
        db.session.commit()

        # Create Memos
        memos = []
        for _ in range(10):
            sender = rc(users)
            receiver = rc([u for u in users if u != sender])  # Avoid self-sending memos
            memo = Memo(
                sender_id=sender.id,
                receiver_id=receiver.id,
                content=fake.paragraph()
            )
            memos.append(memo)
        db.session.add_all(memos)
        db.session.commit()

        print("Seed complete!")

