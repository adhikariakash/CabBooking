"""Class  containing the models of the console application."""
from src.configuration.config import db


class User(db.Model):
    """
    Implementation of user model.
    """
    username = db.Column(db.String(200), primary_key=True)
    emp_id = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200))
    type = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    is_deleted = db.Column(db.String(200))


class cab(db.Model):
    """
        Implementation of cab model.
    """
    cab_number = db.Column(db.String(200), primary_key=True)
    capacity = db.Column(db.Integer)
    is_deleted = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)


class routes(db.Model):
    """
        Implementation of routes model.
    """
    id = db.Column(db.Integer, primary_key=True)
    cab_number = db.Column(db.String(200))
    route_id = db.Column(db.String(200))
    stop_name = db.Column(db.String(200))
    stage = db.Column(db.Integer)
    time = db.Column(db.String(200))
    available_seats = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)
    is_deleted = db.Column(db.String(200))


class booking(db.Model):
    """
        Implementation of booking model.
    """
    booking_id = db.Column(db.String(200), primary_key=True)
    emp_id = db.Column(db.String(200))
    cab_number = db.Column(db.String(200))
    source = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    arrival_time = db.Column(db.String(200))
    departure_time = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    canceled = db.Column(db.String(200))
