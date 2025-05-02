from app import db
from sqlalchemy import ForeignKeyConstraint, CheckConstraint

class Address(db.Model):
    __tablename__ = 'address'
    street = db.Column(db.String(100), primary_key=True)
    number = db.Column(db.String(10), primary_key=True)
    city = db.Column(db.String(100), primary_key=True)

class Manager(db.Model):
    __tablename__ = 'managers'
    ssn = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class ClientAddress(db.Model):
    __tablename__ = 'clientaddress'
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), primary_key=True)
    street = db.Column(db.String(100), primary_key=True)
    number = db.Column(db.String(10), primary_key=True)
    city = db.Column(db.String(100), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['street', 'number', 'city'],
            ['address.street', 'address.number', 'address.city']
        ),
    )

class CreditCard(db.Model):
    __tablename__ = 'creditcard'
    card_number = db.Column(db.String(20), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['street', 'number', 'city'],
            ['address.street', 'address.number', 'address.city']
        ),
    )

class Car(db.Model):
    __tablename__ = 'cars'
    carid = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    models = db.relationship("Model", backref="car", cascade="all, delete-orphan", lazy=True)

class Model(db.Model):
    __tablename__ = 'models'
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid'), primary_key=True)
    modelid = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False)
    construction_year = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(10), nullable=False)

class Driver(db.Model):
    __tablename__ = 'driver'
    driverid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['street', 'number', 'city'],
            ['address.street', 'address.number', 'address.city']
        ),
    )

class DriverModel(db.Model):
    __tablename__ = 'drivermodel'
    driverid = db.Column(db.Integer, db.ForeignKey('driver.driverid'), primary_key=True)
    carid = db.Column(db.Integer, primary_key=True)
    modelid = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['carid', 'modelid'],
            ['models.carid', 'models.modelid']
        ),
    )

class Rent(db.Model):
    __tablename__ = 'rent'
    rent_id = db.Column(db.Integer, primary_key=True)
    rent_date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    driverid = db.Column(db.Integer, db.ForeignKey('driver.driverid'), nullable=False)
    carid = db.Column(db.Integer, nullable=False)
    modelid = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['carid', 'modelid'],
            ['models.carid', 'models.modelid']
        ),
        db.UniqueConstraint('rent_date', 'driverid'),
        db.UniqueConstraint('rent_date', 'carid'),
    )

class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True)
    driverid = db.Column(db.Integer, db.ForeignKey('driver.driverid'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    rent_id = db.Column(db.Integer, db.ForeignKey('rent.rent_id'), nullable=False)
    message = db.Column(db.Text)
    rating = db.Column(db.Integer, CheckConstraint('rating >= 0 AND rating <= 5'))

    __table_args__ = (
        db.UniqueConstraint('driverid', 'client_id', 'rent_id'),
    )
