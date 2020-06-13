"""Contains the functionalities of the admin."""
import uuid
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from src.handler.utilities import Register
from src.models.models import User, cab, booking, routes
from src.configuration.config import db_url
from src.utils.Enums import Input
import pandas as pd
from collections import defaultdict
from sqlalchemy.inspection import inspect

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


class Admin:
    def selection(self):
        """
        Selection of features for Employee.
        :return: True/False
        """
        ch = ''
        while ch != '8':
            ch = input(Input.user_choice.value)
            switcher = {
                '1': 'self.create_employee()',
                '2': 'self.update_employee()',
                '3': 'self.delete_employee()',
                '4': 'self.add_new_cab()',
                '5': 'self.employee_bookings()',
                '6': 'self.add_routes()',
                '7': 'self.delete_routes()',
                '8': "print('Exiting admin!')",
            }
            eval(switcher.get(ch, "print('Invalid choice')"))
        return True

    def create_employee(self):
        """
        Function to create employee.
        """
        if Register().newUser("employee"):
            return True
        return False

    def update_employee(self, sess):
        """
        Function to update the employee details.
        """
        try:
            print("Update employee")
            Register().list_of_employee()
            username = input(Input.update_username.value)
            print(username)
            passwrd = input(Input.update_password.value)
            session.query(User).filter(User.username == username).update({'password': passwrd})
            session.commit()
            print(Input.password_updated.value)
            return True
        except exc.SQLAlchemyError as e:
            print("Error updating employee : {}".format(e))
            return False

    def delete_employee(self, sess):
        """
        Function to delete the employee.
        """
        try:
            print("Delete employee")
            Register().list_of_employee()
            username = input(Input.delete_username.value)
            session.query(User).filter(User.username == username).update({'is_deleted': True})
            session.commit()
            print(Input.employee_deleted.value)
            print(username)
            return True
        except exc.SQLAlchemyError as e:
            print("Error while deleting employee : {}".format(e))
            return False

    def add_new_cab(self, sess):
        """
        Function to add a new cab.
        """
        try:
            print("Adding a new cab")
            cab_number = input(Input.cab_number.value)
            capacity = int(input(Input.capacity.value))
            new_cab = cab(cab_number=cab_number, capacity=capacity, is_deleted="False")
            session.add(new_cab)
            session.commit()
            print(Input.cab_added.value)
            return True
        except exc.SQLAlchemyError as e:
            print("Error while deleting employee : {}".format(e))
            return False

    def employee_bookings(self, sess):
        """
        Function to check the bookings of a particular employee.
        """
        try:
            print("Bookings of a particular employee")
            Register().list_of_employee()
            emp_id = input(Input.emp_id.value)
            bookings = session.query(booking).filter(booking.emp_id == emp_id).all()
            df = pd.DataFrame(bookings)
            print(df)

            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print("Error with list : {}".format(e))
            return False

    def add_routes(self, sess):
        """
        Function to add routes.
        """
        try:
            print("Add routes for the cab")
            Register().list_of_cabs()
            cab_number = input(Input.cab_number.value)
            no_of_Stops = int(input(Input.stops.value))
            route_id = str(uuid.uuid4())
            i = 0
            while i != no_of_Stops:
                y = 0
                stop_name = input(Input.stop_name.value)
                stage = int(input(Input.number_of_stops.value))
                timing = input(Input.time_input.value)
                available_seat = session.query(cab).filter(cab.cab_number == cab_number).all()
                for row in available_seat:
                    y = row.capacity
                route_of_car = routes(cab_number=cab_number, route_id=route_id, stop_name=stop_name, stage=stage,
                                      time=timing, available_seats=y,
                                      is_deleted="false")
                session.add(route_of_car)
                i += 1
            session.commit()
            print(Input.routes_added.value)
            return True
        except exc.SQLAlchemyError as e:
            print("Error while adding routes : {}".format(e))
            return False

    def delete_routes(self):
        """
        Function to delete the routes.
        """
        try:
            Register().list_of_routes()
            route_id = input(Input.route_id.value)
            session.query(routes).filter(routes.route_id == route_id).update({'is_deleted': True})
            session.commit()
            print("Route is deleted")
            return True
        except exc.SQLAlchemyError as e:
            print("Error while deleting routes : {}".format(e))
            return False
