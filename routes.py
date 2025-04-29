from flask import render_template, request
from models import Person

def register_routes(app, db):
    @app.route('/')
    def index():
        people = Person.query.all()
        return render_template('index.html', people=people)