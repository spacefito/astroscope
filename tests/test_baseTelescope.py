from unittest import TestCase
from testfixtures import replace
from telescopes import BaseTelescope
from mock import Mock
import time

class TestBaseTelescope(TestCase):
    def setUp(self):
        self.dut = BaseTelescope()

    @replace('telescopes.BaseTelescope.get_alt_az', Mock())
    @replace('telescopes.BaseTelescope.get_time_initializer', Mock())
    @replace('telescopes.BaseTelescope.get_location_lat_long', Mock())
    def test_get_altaz(self, mock_lat_long, mock_time_init, mock_alt_az):
        mock_alt_az.return_value = set([1.0, 2.0])
        mock_lat_long.return_value = set([37.5, -121.0])
        mock_time_init.return_value = time.time()

        print(self.dut.get_altaz())
