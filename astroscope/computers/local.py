import requests
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation

class LocalComputer(object):

    def get_time(self):
        return Time(self.get_time_initializer(),
                    location=self.get_earth_location())

    def find_view_in_catalog(self, output_filename):
        _radec = self.get_radec()
        impix = 1024
        imsize = 12 * u.arcmin
        cutoutbaseurl = 'http://skyservice.pha.jhu.edu/DR12/ImgCutout/' \
                        'getjpeg.aspx'
        userdata = dict(ra=_radec.ra.deg, dec=_radec.dec.deg, width=impix,
                        height=impix, scale=imsize.to(u.arcsec).value / impix)
        resp = requests.get(cutoutbaseurl, userdata)
        with open(output_filename, 'wb') as f:
            for chunck in resp:
                f.write(chunck)

    def get_earth_location(self):
        """Returns astropy EarthLocation object

        :return astropy EarthLocation object containg
        telescopes earth location"""
        latitude, longitude = self.get_location_lat_long()
        return EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg)

    def get_azalt(self):
        """Returns Horizontal SkyCoord

         :return Astropy Horizontal SkyCoord of telescope

         """
        _az, _alt = self.get_az_alt()
        _altaz = SkyCoord(alt=_alt * u.deg,
                          az=_az * u.deg,
                          frame='altaz',
                          obstime=Time.now(),
                          location=self.get_earth_location())
        return _altaz

    def goto_azalt(self, altaz):
        self.goto_az_alt(altaz.az.degree, altaz.alt.degree)

    def SkyCoordRaDec(self, ra, dec):
        return SkyCoord(ra=_ra * u.deg, dec=_dec * u.deg, frame="icrs")