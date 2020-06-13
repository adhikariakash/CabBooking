from unittest.mock import patch
from unittest import TestCase
from src.handler.employee import Employee


class TestEmployee(TestCase):

    def setUp(self):
        self.emp_id = '123'

    @patch('src.handler.utilities.Register.view_rides')
    def test_view_ride(self, view_rides):
        view_rides.return_value = False
        assert Employee(self.emp_id).view_ride() is False

