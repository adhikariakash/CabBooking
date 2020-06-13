"""Implementation of employee class containing the functionalities of an employee."""
from src.handler.utilities import Register
from src.utils.Enums import Input
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.configuration.config import db_url

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


class Employee:

    def __init__(self, emp_id):
        self.emp_id = emp_id

    def selection(self):
        """
        Selection of features for Employee
        :return: True/False
        """
        ch = ''
        while ch != '4':
            print(Input.user_selection.value)
            ch = input(Input.action.value)
            switcher = {
                '1': 'self.cab_booking()',
                '2': 'self.view_ride()',
                '3': 'self.cancel_ride()',
                '4': "print('Exit Employee')"
            }
            eval(switcher.get(ch, "print('Invalid choice')"))

    def cab_booking(self):
        """
        Cab booking functionality.
        """
        if Register().get_avl_cab(self.emp_id, session):
            return True
        return False

    def view_ride(self):
        """
        Function to view rides.
        """
        if Register().view_rides(self.emp_id):
            return True
        return False

    def cancel_ride(self):
        """
        Function to cancel ride.
        """
        if Register().cancel_ride(self.emp_id):
            return True
        return False
