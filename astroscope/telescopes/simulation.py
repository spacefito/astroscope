import astroscope.telescopes
import time


class FakeTelescope(astroscope.telescopes.BaseTelescope):

    _location_lat = 0.0
    _location_long = 0.0
    _time = None
    _is_aligned = False
    _response = "#"
    _ra = 0.0
    _dec = 0.0
    _az = 0.0
    _alt = 0.0
    _operation_in_progress = False
    _received_commands = []
    _outputs = []
    _internal_counter = None

    def read_response(self):
        return self._response

    def is_aligned(self):
        return self._is_aligned

    def get_ra_dec(self):
        return self._ra, self._dec

    def get_az_alt(self):
        return self._alt, self._az

    def cancel_current_operation(self):
        self._operation_in_progress = False
        return self._response

    def get_location_lat_long(self):
        return self._location_lat, self._location_long

    def set_location_lat_long(self, _lat, _long):
        self._location_lat = _lat
        self._location_long = _long

    def goto_ra_dec(self, _ra, _dec):
        self._ra = _ra
        self._dec = _dec
        self._response = "#"

    def goto_az_alt(self, _az, _alt):
        self._alt = _alt
        self._az = _az
        self._response = "#"

    def get_time_initializer(self):
        return time.time()

    def display(self, msg):
        self._outputs.append(msg)
        self._response = "#"

    def set_time_initializer(self, _time):
        self._time = _time
        self._internal_counter = time.time()

    def send_command(self, cmd):
            self._received_commands.append(cmd)

