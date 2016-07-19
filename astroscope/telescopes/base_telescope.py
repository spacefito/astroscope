
class TelescopeError(Exception):
    def __init__(self, msg):
        self._msg = msg


class TelescopeCommand(object):

    def __init__(self, cmd):
        self._cmd = cmd

# noinspection PyUnresolvedReferences
class BaseTelescope(object):
    """Base class for telescope"""

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

    def cancel_current_operation(self):
        """Cancels any current operation the telescope is performing"""
        raise NotImplementedError

    def get_location_lat_long(self):
        """Returns telescope location in latitude and longitude.

        :return: object with latitude andlongitude information.
        """
        raise NotImplementedError

    def set_location_lat_long(self, lat, lon):
        """Sets telescope locatoin (lat and long) to provided earth location

        :param lon:
        :param lat:
        :return: object containing any error or other pertinent information
        """
        raise NotImplementedError

    def get_earth_location(self):
        """Returns astropy EarthLocation object

        :return astropy EarthLocation object containg
        telescopes earth location"""
        raise NotImplementedError

    def get_ra_dec(self):
        """Returns Right Ascension and Declination telescope is pointing at

        :return: object with right ascension and declination information.
        """
        raise NotImplementedError

    def get_radec(self):
        """Returns astropy spherical SkyCoord

        :return astropy SkyCoord object with in spherical
                coordinates
        """
        raise NotImplementedError

    def goto_ra_dec(self, _ra, _dec):
        """Points telescope to provided radec.

        :param _dec:
        :param _ra:
        :return: object containing any error or other pertinent information
        """
        raise NotImplementedError

    def goto_radec(self, _radec):
        self.goto_ra_dec(_radec.ra.degree, _radec.dec.degree)

    def get_az_alt(self):
        """Gets Altitude (elevation) and azimuth telescope is pointing to
        :return: object with alt az information.
        """
        raise NotImplementedError

    def get_azalt(self):
        """Returns Horizontal SkyCoord

         :return Astropy Horizontal SkyCoord of telescope

         """
        raise NotImplementedError

    def goto_az_alt(self, _alt, _az):
        """Points telescope to provided Alt/Ax coodinates.

        :param _az:
        :param _alt:
        :return: object containing any error or other pertinent information
        """
        raise NotImplementedError

    def move_alt_by(self, degs):
        _az, _alt = self.get_az_alt()
        new_alt = _alt + float(degs)
        self.goto_az_alt(_az, new_alt)

    def move_az_by(self, degs):
        _az, _alt = self.get_az_alt()
        new_az = _az + float(degs)
        self.goto_az_alt(new_az, _alt)

    def get_time_initializer(self):
        """ Returns an object which can be used to create a astropy.Time object

        :return: time initilizer object
        """
        raise NotImplementedError

    def set_time_initializer(self, _time):
        """Configures time on telescope
        :param _time:
        :return: object containing any error or other pertinent information
        """
        raise NotImplementedError

    def set_time(self, _time):
        self.set_time_initializer(_time.unix)

    def display(self, msg):
        """Display message on telescope's control display

        :param msg: message to be displayed.
        :return: object containing any error or other pertinent information
        """
        raise NotImplementedError

    def verify_connection(self):
        raise NotImplementedError

    def get_time(self):
        """ Returns astropy Time object with current telescope time
        :return astropy.Time
        """
        raise NotImplementedError
