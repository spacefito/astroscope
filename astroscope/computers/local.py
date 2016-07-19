import requests
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation

class LocalComputer(object):

    def find_view_in_catalog(self, output_filename):
        """Fetches picture from online catalogs of current location telescope is pointing to
        
        :param output_filename: the filename to save picture to
        """
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

    def SkyCoordRaDec(self, ra, dec):
        return SkyCoord(ra=_ra * u.deg, dec=_dec * u.deg, frame="icrs")
