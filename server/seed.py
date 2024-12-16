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
        print("Clearing existing data...")
        db.session.query(Memo).delete()
        db.session.query(Invoice).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Seed Specific Users
        print("Creating specific users...")
        specific_users = [
            User(name="Alice Doe", email="alice@gmail.com", password="password123"),
            User(name="Bob Smith", email="bob@gmail.com", password="password123"),
            User(name="Charlie Brown", email="charlie@gmail.com", password="password123"),
            User(name="Daisy Green", email="daisy@gmail.com", password="password123"),
            User(name="Eve White", email="eve@gmail.com", password="password123"),
        ]
        db.session.add_all(specific_users)
        db.session.commit()

        # Seed Random Users
        print("Creating random users...")
        random_users = []
        for i in range(10):  # Create 10 random users
            user = User(
                name=fake.name(),
                email=f"user{i}@gmail.com",  # Ensuring unique, simple emails for testing
                password="password"  # Use hashed passwords in production
            )
            random_users.append(user)
        db.session.add_all(random_users)
        db.session.commit()

        # Combine users for further relationships
        users = specific_users + random_users

        # Seed Invoices
        print("Creating invoices...")
        invoices = []
        for _ in range(20):  # Create 20 invoices
            sender = rc(users)
            receiver = rc([u for u in users if u != sender])  # Ensure sender and receiver are different
            invoice = Invoice(
                sender_id=sender.id,
                receiver_id=receiver.id,
                amount=round(fake.random_number(digits=4, fix_len=False) + fake.pyfloat(right_digits=2, positive=True), 2),  # Random realistic amount
                description=f"Invoice for {fake.bs().capitalize()}"  # Use a realistic business term
            )
            invoices.append(invoice)
        db.session.add_all(invoices)
        db.session.commit()

        # Seed Memos
        print("Creating memos...")
        memos = []
        for _ in range(20):  # Create 20 memos
            sender = rc(users)
            receiver = rc([u for u in users if u != sender])  # Ensure sender and receiver are different
            memo = Memo(
                sender_id=sender.id,
                receiver_id=receiver.id,
                content=f"Memo regarding {fake.catch_phrase().capitalize()}"  # Use realistic content
            )
            memos.append(memo)
        db.session.add_all(memos)
        db.session.commit()

        print("Seed complete! Database populated with users, invoices, and memos.")




