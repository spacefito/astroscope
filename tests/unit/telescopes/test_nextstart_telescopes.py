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
        self.telescope._validate_command("#")
        self.assertRaises(AssertionError,
                          self.telescope._validate_command,
                          "This should fail"
                          )
