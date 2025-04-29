from app import db

# placeholder
class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# test
def __repr__(self):
    return f"Person with id: {self.id}, name: {self.name}, and age: {self.age}"
    