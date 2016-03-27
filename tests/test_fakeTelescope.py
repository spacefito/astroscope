from unittest import TestCase
import simulation
import time

class TestFakeTelescope(TestCase):

    def setUp(self):
        self.dut = simulation.FakeTelescope()
        self._test_lat = 2.0
        self._test_long = 6.0
        self._test_ra = 10.0
        self._test_dec = 20.0
        self._test_alt = 45.0
        self._test_az = 240.0
        self._test_command = "test_command"

    def test_is_aligned(self):
        self.dut.is_aligned()

    def test_get_ra_dec(self):
        self.dut.get_ra_dec()

    def test_cancel_current_operation(self):
        self.dut.cancel_current_operation()

    def test_get_and_set_location_lat_long(self):
        self.dut.set_location_lat_long(self._test_lat, self._test_long)
        _lat, _long = self.dut.get_location_lat_long()
        self.assertEqual(self._test_lat, _lat)
        self.assertEqual(self._test_long, _long)

    def test_goto_ra_dec(self):
        self.dut.goto_radec(self._test_ra, self._test_dec)

    def test_get_and_set_time_initializer(self):
        self.dut.get_time_initializer()

    def test_display(self):
        self.dut.display("fake_display")

    def test_set_time(self):
        self.dut.set_time_initializer(time.time())

    def test_send_command(self):
        self.dut.send_command(self._test_command)

    def test_read_response(self):
        self.dut.read_response()
