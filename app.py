from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

DATABASE_URI = os.getenv('DATABASE_URL')

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__, template_folder='templates')

    # db configuration
    # db connection URI uses the format: "dialect://username:password@host:port/database"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    db.init_app(app)

    # import now to avoid circular imports
    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app


