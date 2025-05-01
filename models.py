from app import db
from sqlalchemy import ForeignKeyConstraint

# placeholder
class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Manager class with ssn as primary key, name, and email
class Manager(db.Model):
    __tablename__ = 'managers'
    ssn = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# Car class with car ID as primary key, and brand
class Car(db.Model):
    __tablename__ = 'cars'
    carid = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    models = db.relationship('Model', backref='car', cascade="all, delete")

# Model class with model ID as primary key, car ID as a foreign key, color, construction year, and transmission
class Model(db.Model):
    __tablename__ = 'models'
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid'), primary_key=True)
    modelid = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False)
    construction_year = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(10), nullable=False)

# Driver class with driverid as the primary key, name, and email. Then street, number, and city as a composite key
class Driver(db.Model):
    __tablename__ = 'driver'
    driverid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['street', 'number', 'city'],
            ['address.street', 'address.number', 'address.city']
        ),
    )

# Address class with street, number, and city as a composite key
class Address(db.Model):
    __tablename__ = 'address'
    street = db.Column(db.String(100), primary_key=True)
    number = db.Column(db.String(10), primary_key=True)
    city = db.Column(db.String(100), primary_key=True)

# test
def __repr__(self):
    return f"Person with id: {self.id}, name: {self.name}, and age: {self.age}"
    