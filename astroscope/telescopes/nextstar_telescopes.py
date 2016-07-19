import serial

from base_telescope import BaseTelescope


class TelescopeError(Exception):
    def __init__(self, msg):
        self.msg = msg


class TelescopeCommand(object):
    _cmd = ""


class NexStarSLT130(BaseTelescope ):
    time_format = 'isot'

    def __init__(self, device):
        super(NexStarSLT130, self).__init__(device)
        self.serial = serial.Serial(device, baudrate=9600, timeout=2)
        self.DIR_AZIMUTH = 0
        self.DIR_ELEVATION = 1

    def send_command(self, cmd):
        """Sends cmd to the telescope
        
        :param cmd: is a string formated to represent a command
                    The content of cmd is not checked so caller
                    must asure cmd is valid and validate response 
                    if necessary
        """
        self.serial.write(cmd)

    def read_response(self, n_bytes=1):
        """ Reads response from telescope

        :param n_bytes: the number of bytes to read form the telescope's
                        response
        :return : n_bytes number of bytes from response or None if error
        """
        return self.serial.read(n_bytes)

    @staticmethod
    def _validate_command(response):
        """ Validates telescope received command
        
        Telescope acknowledges command is valid by returning the # sign
        """
        assert response == '#', 'Command failed'

    @staticmethod
    def _convert_hex_to_percentage_of_revolution(string):
        """ Converts 32 bit hex to percentage of 360 degrees """
        return int(string, 16) / 2. ** 32 * 360.

    @staticmethod
    def _convert_to_percentage_of_revolution_in_hex(degrees):
        """ Coverts percentage of 360 degree revolution to hex """
        rounded = round(degrees / 360. * 2. ** 32)
        return '%08X' % rounded

    def _get_position(self, coordinate_system):
        """Returns telescope postion in the requested coordinate system.
        
        :param coordinate_system: the desired coordinate systems. Possible values
                                  are e= spherical (radec) or z = Horizontal(azalt)

        :return : tuple with desired coordinates in the form of (ra, dec) or (az, alt)
        """
        self.send_command(coordinate_system)
        response = self.read_response(18)
        return (self._convert_hex_to_percentage_of_revolution(response[:8]),
                self._convert_hex_to_percentage_of_revolution(response[9:17]))

    def get_az_alt(self):
        """ Returns Horizontal coordinates telescope is pointing to
        
        :return (az, alt)
        """
        return self._get_position('z')

    def get_ra_dec(self):
        """ Returns Spherical coordinates telescope is pointing to
        
        :return (ra, dec)
        """
        return self._get_position('e')

    def _goto_command(self, char, values):
        """ Points telescope to given coordinates in given coordinate system
        
        :param char: selects coordinate system. Possible values
                     are r= spherical (radec) or b = Horizontal(azalt)
                     
        :return boolean: True - command was received by telescope. False - command failed.
        """
        command = (char + self._convert_to_percentage_of_revolution_in_hex(
            values[0]) + ',' +
                   self._convert_to_percentage_of_revolution_in_hex(values[1]))
        self.send_command(command)
        response = self.read_response(1)
        return "#" in response

    def goto_az_alt(self, az, alt):
        """ Points telescope to Horizontal coordinates (az, alt)
        
        :param  az: azimuth expressed as a hex string equal to the 
                    percentage of a 360 degree circle
                    
        :param alt: elevation expressed as a hex string equal to the 
                    percentage of a 360 degree circle
        """
        self._goto_command('b', (az, alt))

    def goto_ra_dec(self, ra, dec):
        """ Points telescope to Speherical coordinates
        
        :param  ra: Right ascention expressed as a hex string equal
                    to the percentage of a 360 degree circle
                    
        :param dec: Declination expressed as a hex string equal
                    to the percentage of a 360 degree circle
        """
        self._goto_command('r', (ra, dec))

    def sync(self, ra, dec):
        """Sets sync on telescope to given spherical coordinates
        
        :param  ra: Right ascention expressed as a hex string equal
                    to the percentage of a 360 degree circle
                    
        :param dec: Declination expressed as a hex string equal
                    to the percentage of a 360 degree circle
        """
        self._goto_command('s', (ra, dec))

    def get_tracking_mode(self):
        """ Get tracking mode of telescope
        
        :return string representing tracking mode
        """
        self.send_command('t')
        response = self.read_response(2)
        return ord(response[0])

    def set_tracking_mode(self, mode):
        """ Sets tracking mode on telescope
        
        :param mode: integer representing desired tracking mode
        """
        self.send_command('T' + chr(mode))
        response = self.read_response(1)
        self._validate_command(response)

    def _var_slew_command(self, direction, rate):
        """ Sets the variable slew rate of telescope on given axis
        
        :param direction: axis of slew. either DIR_AZIMUTH or DIR_ELEVATION
        
        :param rate: rate of slew 
        """
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
        """ Sets the variable slew rate of telescope in Horizontal coordinates
        
        :param az_rate: slew rate in te azimuth axies
        
        :param el_rate: slew rate in the elevation axis
        """
        self._var_slew_command(self.DIR_AZIMUTH, az_rate)
        self._var_slew_command(self.DIR_ELEVATION, el_rate)

    def _fixed_slew_command(self, direction, rate):
        """ Sets the fixed slew rate of telescope on given axis
        
        :param direction: axis of slew. either DIR_AZIMUTH or DIR_ELEVATION
        
        :param rate: rate of slew
        """
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
        """ Sets the fixed slew rate of telescope in Horizontal coordinates
        
        :param az_rate: slew rate in te azimuth axies
        
        :param el_rate: slew rate in the elevation axis
        """
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

        :return: (lat_degrees, long_degrees)
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
        """ Sets location of telescope
        
        :param lat: lattitude
        :param lon: longitude
        """
        command = 'W'
        for p in lat:
            command += chr(p)
        for p in lon:
            command += chr(p)
        self.send_command(command)
        response = self.read_response(1)
        self._validate_command(response)

    def _get_time(self):
        """ Reads time from telescope
        
        :return time string
        """
        self.send_command('h')
        response = self.read_response(9)
        time = ()
        for char in response[:-1]:
            time = time + (ord(char),)
        return time

    def get_time_initializer(self):
        """Returns time initializer derived from telescope's time
        
        :return string of the format YYYYMMDDTHHmmss
        """
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

    def set_time_initializer(self, time):
        """ Sets time on telescope
        
        :param time: time initilizer string of format YYYMMDDTHHmmss
        """
        command = 'H'
        for p in time:
            command += chr(p)
        self.send_command(command)
        response = self.read_response(1)
        self._validate_command(response)

    def get_version(self):
        """Gets telescope software version
        
        :return string representing software version
        """
        self.send_command('V')
        response = self.read_response(3)
        return ord(response[0]) + ord(response[1]) / 10.0

    def get_model(self):
        """Gets telescope model
        
        :return string representing telescopes model
        """
        self.send_command('m')
        response = self.read_response(2)
        return ord(response[0])

    def echo(self, x):
        """Displays message on telescopes LCD
        
        :param x: message to be displayed
        :return response from telescope
        """
        command = 'K' + chr(x)
        self.send_command(command)
        response = self.read_response(2)
        return ord(response[0])

    def alignment_complete(self):
        """ Checks to see if the telescope alignement is complete
        
        :return True of alignment is complete, False otherwise
        """
        self.send_command('J')
        response = self.read_response(2)
        return True if ord(response[0]) == 1 else False

    def goto_in_progress(self):
        """Checks to see if there is a "goto" operation in progress on telescope
        
        :return True if there is a current "goto" in progress, False otherwise
        """
        self.send_command('L')
        response = self.read_response(2)
        return True if int(response[0]) == 1 else False

    def cancel_goto(self):
        """Cancels any "goto" operation in progress
        
        If there is a "goto" operation in progress on the telescope
        it is cancelled
        """
        self.send_command('M')
        response = self.read_response(1)
        self._validate_command(response)

    def cancel_current_operation(self):
        """Cancels current operations on telescope"""
        self.cancel_goto()

    def display(self, msg):
        """displays message on telescopes interface
        
        :param msg: message to be display
        """
        print(self.echo(msg))

    def goto_azalt(self, altaz):
        """Points telescope to given Horizontal coordinates
        
        :param altaz: astropy SkyCoordinate object representing the coordinates
        """
        #TODO(spacefito): this needs to be moved to the local_telescope as it is dependent on astropy
        self.goto_az_alt(altaz.az.deg, altaz.el.deg)

