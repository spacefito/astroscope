from unittest import TestCase
import mock
import serial
from astroscope.telescopes.nextstar_telescopes import NexStarSLT130

class TestNexStarSLT130(TestCase):

    @mock.patch.object(serial, 'Serial')
    def setUp(self, mocked_serial):
        self.serial_device = mock.Mock()
        self.telescope = NexStarSLT130(self.serial_device)
        mocked_serial.assert_called_with(self.serial_device,
                                         baudrate=9600,
                                         timeout=2)
        self.serial  = self.telescope.serial
        pass

    def test___init__(self):
        self.assertEqual(self.telescope.DIR_AZIMUTH, 0)
        self.assertEqual(self.telescope.DIR_ELEVATION,1)

    @mock.patch.object(serial.Serial, 'write')
    def test_send_command(self, mocked_write):
        cmd = mock.Mock()
        self.serial.write = mock.MagicMock()
        self.telescope.send_command(cmd)
        self.serial.write.assert_called_with(cmd)

    def test_read_response(self):
        mocked_response = mock.Mock()
        self.serial.read = mock.MagicMock()
        self.serial.read.return_value = mocked_response
        response = self.telescope.read_response(5)
        self.serial.read.assert_called_with(5)
        self.assertEqual(mocked_response, response)

    def test__validate_command(self):
        self.fail()

    def test__convert_hex_to_percentage_of_revolution(self):
        self.fail()

    def test__convert_to_percentage_of_revolution_in_hex(self):
        self.fail()

    def test__get_position(self):
        self.fail()

    def test_get_az_alt(self):
        self.fail()

    def test_get_ra_dec(self):
        self.fail()

    def test__goto_command(self):
        self.fail()

    def test_goto_az_alt(self):
        self.fail()

    def test_goto_ra_dec(self):
        self.fail()

    def test_sync(self):
        self.fail()

    def test_get_tracking_mode(self):
        self.fail()

    def test_set_tracking_mode(self):
        self.fail()

    def test__var_slew_command(self):
        self.fail()

    def test_slew_var(self):
        self.fail()

    def test__fixed_slew_command(self):
        self.fail()

    def test_slew_fixed(self):
        self.fail()

    def test_get_location_lat_long(self):
        self.fail()

    def test_set_location(self):
        self.fail()

    def test__get_time(self):
        self.fail()

    def test_get_time_initializer(self):
        self.fail()

    def test_set_time_initializer(self):
        self.fail()

    def test_get_version(self):
        self.fail()

    def test_get_model(self):
        self.fail()

    def test_echo(self):
        self.fail()

    def test_alignment_complete(self):
        self.fail()

    def test_goto_in_progress(self):
        self.fail()

    def test_cancel_goto(self):
        self.fail()

    def test_cancel_current_operation(self):
        self.fail()

    def test_display(self):
        self.fail()

    def test_goto_azalt(self):
        self.fail()

    def test_set_location_lat_long(self):
        self.fail()
