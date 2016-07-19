from unittest import TestCase
import astroscope.telescopes.base_telescope as base_telescope
import mock
import astroscope.telescopes.base_telescope


class TestBaseTelescope(TestCase):

    def setUp(self):
        self.telescope = base_telescope.BaseTelescope()

    def test_dec_to_degrees(self):
        degrees_str = str(300) + unichr(176).encode('latin-1')
        minutes_str = str(36) + "'"
        seconds_str = str(21) + '"'
        pre= degrees_str + minutes_str + seconds_str
        res = self.telescope.dec_to_degrees(300.6060)
        self.assertEqual(pre, res)

    def test_cancel_current_operation(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.cancel_current_operation)

    def test_get_location_lat_long(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_location_lat_long)

    def test_set_location_lat_long(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.set_location_lat_long,
                          mock.Mock(),
                          mock.Mock())

    def test_get_earth_location(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_earth_location)

    def test_get_ra_dec(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_ra_dec)

    def test_get_radec(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_radec)

    def test_goto_ra_dec(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.goto_ra_dec,
                          mock.Mock(),
                          mock.Mock()
                          )

    def test_goto_radec(self):
        with mock.patch.object(
                astroscope.telescopes.base_telescope.BaseTelescope,
                'goto_ra_dec') as mocked_goto_ra_dec:
            _radec = mock.Mock()
            _radec.ra.degree = 10
            _radec.dec.degree = 20
            self.telescope.goto_radec(_radec)
            mocked_goto_ra_dec.assert_called_with(10,20)

    def test_get_az_alt(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_az_alt)

    def test_get_azalt(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_azalt)

    def test_goto_az_alt(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.goto_az_alt,
                          mock.Mock(),
                          mock.Mock()
                          )

    def test_move_alt_by(self):
        with mock.patch.object(
                astroscope.telescopes.base_telescope.BaseTelescope,
                'goto_az_alt') as mocked_goto_az_alt, \
                mock.patch.object(
                    astroscope.telescopes.base_telescope.BaseTelescope,
                    'get_az_alt', return_value = (1,1)) as mocked_get_az_alt:
            self.telescope.move_alt_by(10)
            mocked_get_az_alt.assert_called()
            mocked_goto_az_alt.assert_called_with(1,11.0)


    def test_move_az_by(self):
        with mock.patch.object(
                astroscope.telescopes.base_telescope.BaseTelescope,
                'goto_az_alt') as mocked_goto_az_alt, \
                mock.patch.object(
                    astroscope.telescopes.base_telescope.BaseTelescope,
                    'get_az_alt', return_value=(1, 1)) as mocked_get_az_alt:
            self.telescope.move_az_by(10)
        mocked_get_az_alt.assert_called()
        mocked_goto_az_alt.assert_called_with(11.0, 1)

    def test_get_time_initializer(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_time_initializer)

    def test_set_time_initializer(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.set_time_initializer, mock.Mock())

    def test_set_time(self):
        with mock.patch.object(
                astroscope.telescopes.base_telescope.BaseTelescope,
                'set_time_initializer') as mocked_set_time_initializer:
            _time = mock.Mock()
            _time.unix = mock.Mock()
            self.telescope.set_time(_time)
            mocked_set_time_initializer.assert_called_with(_time.unix)

    def test_display(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.display, mock.Mock())

    def test_verify_connection(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.verify_connection)

    def test_get_time(self):
        self.assertRaises(NotImplementedError,
                          self.telescope.get_time)


class TestTelescopeCommand(TestCase):
    def test___init__(self):
        cmd = mock.Mock()
        test_cmd =base_telescope.TelescopeCommand(cmd)
        self.assertEquals(cmd, test_cmd._cmd)


class TestTelescopeError(TestCase):
    def test___init__(self):
        msg = mock.Mock()
        test_err =base_telescope.TelescopeError(msg)
        self.assertEquals(msg, test_err._msg)
