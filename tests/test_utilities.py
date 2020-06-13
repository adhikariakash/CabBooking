from unittest import mock, TestCase
from src.handler.utilities import Register
from src.models.models import booking, routes
from datetime import datetime, timedelta
from doubles import allow

class MockFilter(object):

    def __init__(self):
        self._all = None
        # self.first = None

    def all(self):
        return self._all

    def update(self, placeholder):
        pass

    def first(self):
        pass


class MockQuery(object):

    def __init__(self):
        self._filter = MockFilter()

    def filter(self, placeholder):
        return self._filter


class MockSession(object):

    def __init__(self):
        self._query = MockQuery()

    def query(self, placeholder):
        return self._query

    def add(self, placeholder):
        pass

    def commit(self):
        pass


class TestRegister(TestCase):

    def setUp(self):
        self.emp_id = '123'
        self.dummy_completed = [booking(booking_id='test', emp_id='test', cab_number='test', source='test',
                                        destination='test', arrival_time='test', departure_time='test',
                                        created_at=datetime.now() - timedelta(days=1), updated_at=datetime.now(),
                                        canceled='0')]
        self.dummy_upcoming = [booking(booking_id='test', emp_id='test', cab_number='test', source='test',
                                       destination='test', arrival_time='test', departure_time='test',
                                       created_at=datetime.now(), updated_at=datetime.now(),
                                       canceled='0')]
        self.source = 'A'
        self.destination = 'B'
        self.cab_num = 'AP-31-K-1899'
        self.dummy_routes_data = [routes(id=1, cab_number='AP-31-K-1899', route_id='A-E-1', stop_name='A', stage=1,
                                         time='09:00', available_seats=4, updated_at=datetime(2020, 6, 3, 10, 10, 10),
                                         is_deleted='False'),
                                  routes(id=2, cab_number='AP-31-K-1899', route_id='A-E-1', stop_name='E', stage=1,
                                         time='10:00', available_seats=4, updated_at='2020-05-28 11:41:44',
                                         is_deleted='False')]
        self.dummy_source_route = routes(id=1, cab_number='AP-31-K-1899', route_id='A-E-1', stop_name='A', stage=1,
                                         time='09:00', available_seats=4, updated_at=datetime(2020, 6, 3, 10, 10, 10),
                                         is_deleted='False')
        self.dummy_des_route = routes(id=2, cab_number='AP-31-K-1899', route_id='A-E-1', stop_name='E', stage=1,
                                      time='10:00', available_seats=4, updated_at='2020-05-28 11:41:44',
                                      is_deleted='False')
        self.dummy_avl_source_cabs = [{'cab_number': 'AP-31-K-1899', 'stage_no': 1, 'available_seats': 4,
                                       'start_time': '09:00', 'route_id': 'A-E-1'}]
        self.dummy_avl_des_cabs = [{'cab_number': 'AP-31-K-1899', 'stage_no': 5, 'available_seats': 4,
                                    'route_id': 'A-E-1'}]
        self.dummy_detailed_cabs = [['AP-31-K-1899', '07:00', '2', 'A-E-1']]

    @mock.patch('src.handler.utilities.encrypt_message')
    @mock.patch('src.handler.utilities.input')
    def test_newUser_success(self, inputs, encrypt_message):
        inputs.side_effect = ['test', 'test', 'test']
        encrypt_message.return_value = 'test'
        session = MockSession()
        session.add('')
        assert Register().newUser('employee') is True

    def test_list_of_employee_success(self):
        session = MockSession()
        session.query('').filter('').all()
        assert Register().list_of_employee() is True

    # def test_list_of_cabs_success(self):
    #     session = MockSession()
    #     session.query('').filter('').all()
    #     assert Register().list_of_cabs() is True

    @mock.patch('src.handler.utilities.input')
    def test_get_avl_cabs_works(self, inputs):
        session = MockSession()
        session.query('').filter('')._all = self.dummy_routes_data
        inputs.side_effect = ['A', 'E', '08:45']
        test_class = Register()
        allow(test_class).show_avl_cabs.return_value(True)
        assert test_class.get_avl_cab(self.emp_id, session) is True

    @mock.patch('src.handler.utilities.input')
    def test_get_avl_cabs_fail(self, inputs):
        session = MockSession()
        session.query('').filter('')._all = self.dummy_routes_data
        inputs.side_effect = ['A', 'E', 8]
        test_class = Register()
        allow(test_class).show_avl_cabs.return_value(True)
        assert test_class.get_avl_cab(self.emp_id, session) is False

    @mock.patch('src.handler.utilities.input')
    def test_show_avl_cabs_works(self, inputs):
        session = MockSession()
        inputs.side_effect = ['AP-31-K-1899']
        test_class = Register()
        allow(test_class).book_cab.return_value(True)
        assert test_class.show_avl_cabs(self.emp_id, self.dummy_avl_source_cabs, self.dummy_avl_des_cabs, self.source,
                                        self.destination, session) is True

    @mock.patch('src.handler.utilities.input')
    def test_show_avl_cabs_fail(self, inputs):
        session = MockSession()
        inputs.side_effect = ['AP-31-K-1899']
        test_class = Register()
        allow(test_class).book_cab.return_value(True)
        assert test_class.show_avl_cabs(self.emp_id, self.dummy_avl_source_cabs, None, self.source, self.destination,
                                        session) is False

    # def test_book_cabs_works(self):
    #     session = MockSession()
    #     session.query('').filter('').first()
    #     session.query('').filter('').update('')
    #     session.add('')
    #     session.commit()
    #     test_class = Register()
    #     allow(test_class).show_avl_cabs.return_value(True)
    #     assert test_class.book_cab(self.emp_id, self.cab_num, self.dummy_detailed_cabs, self.source, self.destination,
    #                                session) is True

    def test_book_cabs_fails(self):
        session = MockSession()
        session.query('').filter('')._first = self.dummy_source_route
        session.query('').filter('').update('')
        session.add('')
        session.commit()
        test_class = Register()
        allow(test_class).show_avl_cabs.return_value(True)
        assert test_class.book_cab(self.emp_id, self.cab_num, None, self.source, self.destination,
                                   session) is False

    @mock.patch('src.handler.utilities.Register.completed_rides', return_value=True)
    @mock.patch('src.handler.utilities.Register.upcoming_rides', return_value=True)
    def test_view_rides_success(self, upcoming, completed):
        assert Register().view_rides(self.emp_id) is True

    @mock.patch('src.handler.utilities.Register.view_bookings')
    @mock.patch('src.handler.utilities.Register.ride_status')
    def test_upcoming_rides_success(self, ride_status, view_bookings):
        ride_status.return_value = True
        view_bookings.return_value = self.dummy_upcoming
        assert Register().upcoming_rides(self.emp_id) is True

    @mock.patch('src.handler.utilities.Register.view_bookings')
    @mock.patch('src.handler.utilities.Register.ride_status')
    def test_completed_rides_works(self, ride_status, view_bookings):
        ride_status.return_value = True
        view_bookings.return_value = self.dummy_completed
        assert Register().completed_rides('123') is True

    @mock.patch('src.handler.utilities.Register.cancel_booking')
    @mock.patch('src.handler.utilities.input')
    @mock.patch('src.handler.utilities.Register.time_diff')
    @mock.patch('src.handler.utilities.Register.view_bookings')
    def test_cancel_ride_success(self, view_bookings, time_diff, inputs, cancel_booking):
        view_bookings.return_value = self.dummy_upcoming
        time_diff.return_value = True
        inputs.return_value = 'test'
        cancel_booking.return_value = True
        assert Register().cancel_ride(self.emp_id) is True

    @mock.patch('src.handler.utilities.Register.time_diff')
    @mock.patch('src.handler.utilities.Register.view_bookings')
    def test_cancel_ride_failure(self, view_bookings, time_diff):
        view_bookings.return_value = self.dummy_upcoming
        time_diff.return_value = False
        assert Register().cancel_ride(self.emp_id) is False

    def test_time_diff_true(self):
        assert Register().time_diff('20:00') is True

    # def test_time_diff_false(self):
    #     assert Register().time_diff('17:30') is False

    def test_ride_status_true(self):
        assert Register().ride_status('20:00') is True

    # def test_ride_status_false(self):
    #     assert Register().ride_status('17:00') is False

    def test_view_bookings(self):
        sess = MockSession()
        sess.query('').filter('')._all = self.dummy_completed
        assert Register().view_bookings('123', sess) is self.dummy_completed

    def test_cancel_booking(self):
        session = MockSession()
        session.query('').filter('').update('')
        assert Register().cancel_booking('test', session) is True
