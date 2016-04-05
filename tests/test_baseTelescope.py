import time
import unittest

import mock
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time

import astroscope
from astroscope.telescopes import BaseTelescope


# noinspection PyUnresolvedReferences
class TestBaseTelescope(unittest.TestCase):
    def setUp(self):
        self.dut = BaseTelescope()
        # _alt, _az  = 38.0, -121.0
        # self.dut.get_alt_az = mock.Mock()
        # self.dut.get_alt_az.return_value = (_alt, _az)

        # _obstime = Time(self.dut.get_time_initializer(), format='unix')
        # _location = self.dut.get_earth_location()
        # _altaz = SkyCoord(alt=_alt*u.deg,
        #                   az=_az*u.deg,
        #                   frame='altaz',
        #                   obstime = _obstime,
        #                   location=_location)

    def test_get_time(self):
        timestamp = time.time()
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'get_time_initializer') as mocked_time_init:
            mocked_time_init.return_value = timestamp
            self.dut.time_format = 'unix'
            _obstime = Time(self.dut.get_time_initializer(), format='unix')
            obstime = self.dut.get_time()
            self.assertEqual(_obstime, obstime)

    def test_get_earth_location(self):
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'get_location_lat_long') as mocked_lat_long:
            mocked_lat_long.return_value = (38.0, -121.0)
            dut_location = self.dut.get_earth_location()
            print(dut_location.latitude.deg)
            self.assertEqual(dut_location.latitude.deg, 38.0)
            self.assertEqual(dut_location.longitude.deg, -121.0)

    def test_get_altaz(self):
        import time
        timestamp = time.time()
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'get_az_alt') as mocked_alt_az, \
                mock.patch.object(astroscope.telescopes.BaseTelescope,
                                  'get_time_initializer') as mocked_time_init,\
                mock.patch.object(astroscope.telescopes.BaseTelescope,
                                  'get_location_lat_long') as mocked_lat_long:
            mocked_alt_az.return_value = (89.0, 45.0)
            mocked_time_init.return_value = timestamp
            mocked_lat_long.return_value = (38.0, -121.0)
            self.dut.time_format = 'unix'
            # dut_time = self.dut.get_time()
            dut_location = self.dut.get_earth_location()
            _az, _alt = self.dut.get_az_alt()
            altaz = self.dut.get_azalt()
            self.assertEqual(altaz.alt.deg, _alt)
            self.assertEqual(altaz.az.deg, _az)
            self.assertEqual(altaz.location, dut_location)

    def test_get_radec(self):
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'get_ra_dec') as mocked_ra_dec:
            mocked_ra_dec.return_value = (216.0, 45.0)
            radec = self.dut.get_radec()
            self.assertEqual(radec.ra.deg, 216.0)
            self.assertEqual(radec.dec.deg, 45.0)

    def test_goto_altaz(self):
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'goto_az_alt') as mocked_goto_az_alt:
            _alt, _az = 38.0, 239.0
            mocked_goto_az_alt.return_value = True
            _altaz = SkyCoord(alt=_alt * u.deg,
                              az=_az * u.deg,
                              frame="altaz")
            self.dut.goto_azalt(_altaz)
            mocked_goto_az_alt.assert_called_once_with(_az, _alt)

    def test_goto_radec(self):
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'goto_ra_dec') as mocked_goto_ra_dec:
            _ra, _dec = 39.0, 89.0
            mocked_goto_ra_dec.return_value = True
            _radec = SkyCoord(ra=_ra * u.deg, dec=_dec * u.deg, frame="icrs")
            self.dut.goto_radec(_radec)
            mocked_goto_ra_dec.assert_called_once_with(_ra, _dec)

    def test_move_alt(self):
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'get_az_alt') as mocked_get_az_alt, \
                mock.patch.object(astroscope.telescopes.BaseTelescope,
                                  'goto_az_alt') as mocked_goto_az_alt:
            mocked_get_az_alt.return_value = 38.0, 79.0
            mocked_goto_az_alt.return_value = True
            self.dut.move_alt_by(10)
            mocked_goto_az_alt.assert_called_once_with(38.0, 89.0)

    def test_move_az(self):
        with mock.patch.object(astroscope.telescopes.BaseTelescope,
                               'get_az_alt') as mocked_get_az_alt, \
                mock.patch.object(astroscope.telescopes.BaseTelescope,
                                  'goto_az_alt') as mocked_goto_az_alt:
            mocked_get_az_alt.return_value = 38.0, 79.0
            mocked_goto_az_alt.return_value = True
            self.dut.move_az_by(10)
            mocked_goto_az_alt.assert_called_once_with(48.0, 79.0)
