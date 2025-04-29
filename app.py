from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__, template_folder='templates')

    # db configuration
    # db connection URL uses the format: "dialect://username:password@host:port/database"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1473019Sirmono01!@localhost:5432/service'

    db.init_app(app)

    # import now to avoid circular imports
    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app


