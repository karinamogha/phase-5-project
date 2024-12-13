# Standard library imports

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os  # For environment variables

# Local imports

# Flask App Configuration
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Use DATABASE_URL env or fallback to SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Adjust JSON formatting

# SQLAlchemy Metadata Convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Database Initialization
db = SQLAlchemy(metadata=metadata)
db.init_app(app)

# Flask-Migrate Setup
migrate = Migrate(app, db)

# RESTful API Initialization
api = Api(app)

# CORS Setup
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow CORS only for API routes

