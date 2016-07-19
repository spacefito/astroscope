from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation

class AstropyTelescope(object):

    def get_time(self):
        """Get astropy Time object based on telescope settings
        
        Queries telescope for time and location. Returns astropy Time object
        
        :return astropy object based on telescopes time and location
        """
        return Time(self.get_time_initializer(),
                    location=self.get_earth_location())

    def get_earth_location(self):
        """Returns astropy EarthLocation object of telescope

        :return astropy EarthLocation object
        """
        latitude, longitude = self.get_location_lat_long()
        return EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg)

    def get_azalt(self):
        """Returns Horizontal SkyCoord telescope is pointing to

         :return Astropy Horizontal SkyCoord
         """
        _az, _alt = self.get_az_alt()
        _altaz = SkyCoord(alt=_alt * u.deg,
                          az=_az * u.deg,
                          frame='altaz',
                          obstime=Time.now(),
                          location=self.get_earth_location())
        return _altaz

    def goto_azalt(self, altaz):
        """Points telescope to given Horizontal SkyCoord coordinates
        
        :param altaz: astropy SkyCoordinate object representing the coordinates
        """
        self.goto_az_alt(altaz.az.degree, altaz.alt.degree)
