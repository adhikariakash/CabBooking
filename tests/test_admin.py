from unittest import TestCase
import mock
from src.handler.admin import Admin
import random
from src.models.models import booking, User, cab, routes
from datetime import datetime, timedelta


class MockFilter(object):

    def __init__(self):
        self._all = None

    def all(self):
        return self._all


class MockQuery(object):

    def __init__(self):
        self._filter = MockFilter()

    def filter(self, placeHolder):
        return self._filter


class MockSession(object):

    def __init__(self):
        self._query = MockQuery()

    def query(self, placeHolder):
        return self._query

    def add(self, other):
        pass


class TestAdmin(TestCase):
    def setUp(self):
        self.emp_id = '123'
        self.booking_dummy_data = [booking(booking_id='test', emp_id='test', cab_number='test', source='test',
                                           destination='test', arrival_time='test', departure_time='test',
                                           created_at=datetime.now() - timedelta(days=1), updated_at=datetime.now(),
                                           canceled='0')]
        self.user_dummy_data = [User(username='username1', emp_id='emp', password='pass', type='type'
                                     , updated_at=datetime.now(), deleted_at="", is_deleted='false')]
        self.routes_dummy_data = [routes(cab_number='123', route_id='1', stop_name='abcd', stage=4,
                                         time='2020-06-08 15:36:50', available_seats=2,
                                         updated_at='2020-06-08 15:36:50',
                                         is_deleted='False')]
        self.cab_dummy_data = [
            cab(cab_number='123', capacity='4', is_deleted='False', updated_at='2020-06-08 15:36:50', deleted_at="")]

    @mock.patch('src.handler.admin.Admin.update_employee')
    @mock.patch('src.handler.admin.input')
    def test_selection(self, input1, update_employee):
        input1.side_effect = ['2', '8']
        update_employee.return_value = True
        assert Admin().selection() is True

    @mock.patch('src.handler.admin.Register.newUser')
    def test_create_employee(self, newUser):
        newUser.return_value = True
        assert Admin().create_employee() is True

    @mock.patch('src.handler.admin.Register.newUser')
    def test_create_employee_failed(self, newUser):
        newUser.return_value = False
        assert Admin().create_employee() is False

    @mock.patch('src.handler.admin.Register.list_of_employee')
    @mock.patch('src.handler.admin.input')
    def test_update_employee(self, username, listofemployee):
        sess = MockSession()
        listofemployee.return_value = True
        username.side_effect = ["adminqeqwe", "password"]
        sess.query('').filter('')._all = self.user_dummy_data
        assert Admin().update_employee(sess) is True

    # @mock.patch('src.handler.admin.Register.list_of_employee')
    # @mock.patch('src.handler.admin.input')
    # def test_update_employee_failed(self, username, listofemployee):
    #     sess = MockSession()
    #     listofemployee.return_value = True
    #     username.side_effect = ["admin", "password"]
    #
    #     sess.query('').filter('')._all = self.user_dummy_data
    #     assert Admin().update_employee(sess) is False

    @mock.patch('src.handler.admin.Register.list_of_employee')
    @mock.patch('src.handler.admin.input')
    def test_delete_employee(self, inputentry, listofemployee):
        sess = MockSession()
        listofemployee.return_value = True
        inputentry.side_effect = ["adminss", "passwordss"]

        sess.query('').filter('')._all = self.user_dummy_data
        assert Admin().delete_employee(sess) is True

    @mock.patch('src.handler.admin.input')
    def test_add_new_cab(self, input1):
        sess = MockSession()
        randint = str(random.randint(0, 10000))
        print(randint)
        input1.side_effect = [randint, "4"]
        dummy = [{'cab_number': randint, 'capacity': '4', 'is_deleted': 'False'}]
        sess.add(dummy)
        assert Admin().add_new_cab(sess) is True

    @mock.patch('src.handler.admin.input')
    def test_add_new_cab_fail(self, input1):
        sess = MockSession()
        input1.side_effect = ["999", "4"]
        dummy = [{'cab_number': '9999', 'capacity': '4', 'is_deleted': 'False'}]
        sess.add(dummy)
        assert Admin().add_new_cab(sess) is False

    @mock.patch('src.handler.admin.Register.list_of_employee')
    @mock.patch('src.handler.admin.input')
    def test_employee_bookings(self, emp_id, listofemployee):
        sess = MockSession()
        listofemployee.return_value = True
        emp_id.side_effect = "nl-432"
        sess.query('').filter('')._all = {0: [
            {'arrival_time': '20:00', 'booking_id': 'cee05b63-0454-43e4-898e-d15ef6b5c6a3',
             'emp_id': '123', 'created_at': '2020-06-08 15:36:50',
             'canceled': '0'}]}
        assert Admin().employee_bookings(sess) is True

    @mock.patch('src.handler.admin.Register.list_of_routes')
    @mock.patch('src.handler.admin.input')
    def test_delete_routes(self, inputentries, listofroutes):
        session = MockSession()
        listofroutes.return_value = True
        inputentries.side_effect = ["123"]

        session.query('').filter('')._all = {0: [
            {'cab_number': '123', 'capacity': '4', 'is_deleted': 'False'}]}
        dummy = [{'cab_number': '123', 'capacity': '4', 'is_deleted': 'False'}]
        session.add(dummy)
        assert Admin().delete_routes() is True

    @mock.patch('src.handler.admin.Register.list_of_cabs')
    @mock.patch('src.handler.admin.input')
    def test_add_routes(self, inputentries, listofcabs):
        sess = MockSession()
        listofcabs.return_value = True
        inputentries.side_effect = ["123", "1", "1", "123", "123"]
        sess.query('').filter('')._all = self.cab_dummy_data
        dummy = self.routes_dummy_data
        sess.add(dummy)
        assert Admin().add_routes(sess) is True
