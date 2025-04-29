from app import create_app, db
from flask import current_app

app = create_app()
with app.app_context():
    # Check database connection
    result = db.session.execute(db.text("SELECT current_database()")).scalar()
    print(f"Connected to database: {result}")
    
    # Check if table exists
    result = db.session.execute(db.text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'people')")).scalar()
    print(f"'people' table exists: {result}")