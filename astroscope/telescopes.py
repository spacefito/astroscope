from abc import ABCMeta

import serial
import requests
import Image
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.time import Time



class TelescopeError(Exception):
    def __init__(self, msg):
        self.msg = msg


class TelescopeCommand(object):
    _cmd = ""


# noinspection PyUnresolvedReferences
class BaseTelescope(object):
    """Base class for telescope"""
    __metaclass__ = ABCMeta

    @staticmethod
    def dec_to_degrees(dec):
        negative = False
        if dec < 0:
            negative = True
            dec *= -1.0
        _degrees = int(dec)
        degrees_str = str(_degrees) + unichr(176).encode('latin-1')
        if negative:
            degrees_str = "-" + degrees_str
        _minutes = (dec - _degrees) * 60
        minutes_str = str(int(_minutes)) + "'"
        _seconds = (_minutes - int(_minutes)) * 60
        seconds_str = str(int(_seconds)) + '"'
        return degrees_str + minutes_str + seconds_str

    def __init__(self, device="/dev/ttyUSB0"):
        """
        :param device: device which is attached to telescope. Default is
        "/dev/ttyUSB0"
        :return:
        """
        self.device = device

    def find_view_in_catalog(self, output_filename):
        _radec = self.get_radec()
        impix = 1024
        imsize = 12 * u.arcmin
        cutoutbaseurl = 'http://skyservice.pha.jhu.edu/DR12/ImgCutout/' \
                        'getjpeg.aspx'
        userdata= dict(ra=_radec.ra.deg,dec=_radec.dec.deg, width=impix,
                       height=impix, scale=imsize.to(u.arcsec).value / impix)
        resp = requests.get(cutoutbaseurl, userdata)
        with open(output_filename, 'wb') as f:
            for chunck in resp:
                f.write(chunck)

    def cancel_current_operation(self):
        """Cancels any current operation the telescope is performing"""
        pass

    def get_location_lat_long(self):
        """Returns telescope location in latitude and longitude.

        :return: object with latitude andlongitude information.
        """
        pass

    def set_location_lat_long(self, lat, lon):
        """Sets telescope locatoin (lat and long) to provided earth location

        :param lon:
        :param lat:
        :return: object containing any error or other pertinent information
        """
        pass

    def get_earth_location(self):
        latitude, longitude = self.get_location_lat_long()
        return EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg)

    def get_ra_dec(self):
        """Returns Right Ascension and Declination telescope is pointing at

        :return: object with right ascension and declination information.
        """
        pass

    def get_radec(self):
        _ra, _dec = self.get_ra_dec()
        _radec = SkyCoord(ra=_ra * u.deg, dec=_dec * u.deg, frame="icrs")
        return _radec

    def goto_ra_dec(self, _ra, _dec):
        """Points telescope to provided radec.

        :param _dec:
        :param _ra:
        :return: object containing any error or other pertinent information
        """
        pass

    def goto_radec(self, _radec):
        self.goto_ra_dec(_radec.ra.degree, _radec.dec.degree)

    def get_az_alt(self):
        """Gets Altitude (elevation) and azimuth telescope is pointing to
        :return: object with alt az information.
        """
        pass

    def get_azalt(self):
        _az, _alt = self.get_az_alt()
        _altaz = SkyCoord(alt=_alt * u.deg,
                          az=_az * u.deg,
                          frame='altaz',
                          obstime=Time.now(),
                          location=self.get_earth_location())
        return _altaz

    def goto_az_alt(self, _alt, _az):
        """Points telescope to provided Alt/Ax coodinates.

        :param _az:
        :param _alt:
        :return: object containing any error or other pertinent information
        """
        pass

    def move_alt_by(self, degs):
        _az, _alt = self.get_az_alt()
        new_alt = _alt + float(degs)
        self.goto_az_alt(_az, new_alt)

    def move_az_by(self, degs):
        _az, _alt = self.get_az_alt()
        new_az = _az + float(degs)
        self.goto_az_alt(new_az, _alt)

    def goto_azalt(self, altaz):
        self.goto_az_alt(altaz.az.degree, altaz.alt.degree)

    def get_time_initializer(self):
        """ Returns an object which can be used to create a astropy.Time object

        :return: time initilizer object
        """
        return

    def set_time_initializer(self, _time):
        """Configures time on telescope
        :param _time:
        :return: object containing any error or other pertinent information
        """

    def set_time(self, _time):
        self.set_time_initializer(_time.unix)

    def display(self, msg):
        """Display message on telescope's control display

        :param msg: message to be displayed.
        :return: object containing any error or other pertinent information
        """
        pass

    def verify_connection(self):
        pass

    def get_time(self):
        _time_initializer = self.get_time_initializer()
        return Time(_time_initializer, format=self.time_format)



class NexStarSLT130(BaseTelescope):
    time_format = 'isot'


    def __init__(self, device):
        super(NexStarSLT130, self).__init__(device)
        self.serial = serial.Serial(device, baudrate=9600, timeout=2)
        self.DIR_AZIMUTH = 0
        self.DIR_ELEVATION = 1

    def send_command(self, cmd):
        self.serial.write(cmd)
        return True

    def read_response(self, n_bytes=1):
        """ Reads response from telescope

        :param n_bytes: the number of bytes to read form the telescope's
        response
        :return : n_bytes number of bytes from response or None if error
        """
        return self.serial.read(n_bytes)

    @staticmethod
    def _validate_command(response):
        assert response == '#', 'Command failed'

    @staticmethod
    def _convert_hex_to_percentage_of_revolution(string):
        return int(string, 16) / 2. ** 32 * 360.

    @staticmethod
    def _convert_to_percentage_of_revolution_in_hex(degrees):
        rounded = round(degrees / 360. * 2. ** 32)
        return '%08X' % rounded

    def _get_position(self, coordinate_system):
        """Returns telescope postion in the requested coordinate system.

        Possible coordinagte systems are radec(e) and azel(z)

        """
        self.send_command(coordinate_system)
        response = self.read_response(18)
        return (self._convert_hex_to_percentage_of_revolution(response[:8]),
                self._convert_hex_to_percentage_of_revolution(response[9:17]))

    def get_az_alt(self):
        return self._get_position('z')

    def get_ra_dec(self):
        return self._get_position('e')

    def _goto_command(self, char, values):
        command = (char + self._convert_to_percentage_of_revolution_in_hex(
            values[0]) + ',' +
                   self._convert_to_percentage_of_revolution_in_hex(values[1]))
        self.send_command(command)
        response = self.read_response(1)
        return "#" in response

    def goto_az_alt(self, _az, _alt):
        self._goto_command('b', (_az, _alt))

    def goto_ra_dec(self, _ra, _dec):
        self._goto_command('r', (_ra, _dec))

    def sync(self, ra, dec):
        self._goto_command('s', (ra, dec))

    def get_tracking_mode(self):
        self.send_command('t')
        response = self.read_response(2)
        return ord(response[0])

    def set_tracking_mode(self, mode):
        self.send_command('T' + chr(mode))
        response = self.read_response(1)
        self._validate_command(response)

    def _var_slew_command(self, direction, rate):
        negative_rate = True if rate < 0 else False
        track_rate_high = (int(abs(rate)) * 4) / 256
        track_rate_low = (int(abs(rate)) * 4) % 256
        direction_char = chr(16) if direction == self.DIR_AZIMUTH else chr(17)
        sign_char = chr(7) if negative_rate is True else chr(6)
        command = ('P' + chr(3) + direction_char + sign_char +
                   chr(track_rate_high) + chr(track_rate_low) + chr(0) +
                   chr(0))
        self.send_command(command)
        response = self.read_response(1)
        self._validate_command(response)

    def slew_var(self, az_rate, el_rate):
        self._var_slew_command(self.DIR_AZIMUTH, az_rate)
        self._var_slew_command(self.DIR_ELEVATION, el_rate)

    def _fixed_slew_command(self, direction, rate):
        negative_rate = True if rate < 0 else False
        sign_char = chr(37) if negative_rate is True else chr(36)
        direction_char = chr(16) if direction == self.DIR_AZIMUTH else chr(17)
        rate_char = chr(int(abs(rate)))
        command = ('P' + chr(2) + direction_char + sign_char + rate_char +
                   chr(0) + chr(0) + chr(0))
        self.send_command(command)
        response = self.read_response(1)
        self._validate_command(response)

    def slew_fixed(self, az_rate, el_rate):
        assert (az_rate >= -9) and (az_rate <= 9), 'az_rate out of range'
        assert (el_rate >= -9) and (el_rate <= 9), 'az_rate out of range'
        self._fixed_slew_command(self.DIR_AZIMUTH, az_rate)
        self._fixed_slew_command(self.DIR_ELEVATION, el_rate)

    def get_location_lat_long(self):
        """Get location in latitude and longitude

        Positive latitude is above the equator (N), and negative latitude is
        below the equator (S). Positive longitude is east of the prime
        meridian, while negative longitude is west of the prime meridian
        (a north-south line that runs through a point in England)

        If the response contains N = 0 (positive), and E = 0 (positive).

        :return:
        """
        self.send_command('w')
        response = self.read_response(9)

        lat = ()
        for char in response[:4]:
            lat = lat + (ord(char),)
        _lat_degrees = lat[0] + (lat[1] / 60.0) + (lat[2] / (60.0 * 60.0))
        if lat[3] != 0:
            _lat_degrees *= -1.0

        _long = ()
        for char in response[4:-1]:
            _long = _long + (ord(char),)
        _long_degrees = _long[0] + (_long[1] / 60.0) + (
            _long[2] / (60.0 * 60.0))
        if _long[3] != 0:
            _long_degrees *= -1.0

        return _lat_degrees, _long_degrees

    def set_location(self, lat, lon):
        command = 'W'
        for p in lat:
            command += chr(p)
        for p in lon:
            command += chr(p)
        self.send_command(command)
        response = self.read_response(1)
        self._validate_command(response)

    def _get_time(self):
        self.send_command('h')
        response = self.read_response(9)
        time = ()
        for char in response[:-1]:
            time = time + (ord(char),)
        return time

    def get_time_initializer(self):
        """Returns time initializer  of the format YYYYMMDDTHHmmss"""
        (_hour, _minute, _seconds,
         _month, _day_of_month, _year,
         gmt_offset, _DAYLIGHT_SAVINGS_ENABLED) = self._get_time()
        date_string = "20" + str(_year).zfill(2) + "-" + \
                      str(_month).zfill(2) + "-" +\
                      str(_day_of_month).zfill(2) + "T" +\
                      str(_hour).zfill(2) +\
                      ":" + str(_minute).zfill(2) +\
                      ":" + str(_seconds).zfill(2)
        return date_string

    def get_time(self):
        return Time(self.get_time_initializer(),
                    location=self.get_earth_location())

    def set_time_initializer(self, time):
        command = 'H'
        for p in time:
            command += chr(p)
        self.send_command(command)
        response = self.read_response(1)
        self._validate_command(response)

    def get_version(self):
        self.send_command('V')
        response = self.read_response(3)
        return ord(response[0]) + ord(response[1]) / 10.0

    def get_model(self):
        self.send_command('m')
        response = self.read_response(2)
        return ord(response[0])

    def echo(self, x):
        command = 'K' + chr(x)
        self.send_command(command)
        response = self.read_response(2)
        return ord(response[0])

    def alignment_complete(self):
        self.send_command('J')
        response = self.read_response(2)
        return True if ord(response[0]) == 1 else False

    def goto_in_progress(self):
        self.send_command('L')
        response = self.read_response(2)
        return True if int(response[0]) == 1 else False

    def cancel_goto(self):
        self.send_command('M')
        response = self.read_response(1)
        self._validate_command(response)

    def cancel_current_operation(self):
        self.cancel_goto()

    def display(self, msg):
        print(self.echo(msg))

    def goto_azalt(self, altaz):
        self.goto_az_alt(altaz.az.deg, altaz.el.deg)

    def set_location_lat_long(self, lat, lon):
        print "not implemented"
