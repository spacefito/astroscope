#!/usr/bin/env python
import argparse

from astropy import units as u
from astropy.coordinates import AltAz
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.time import Time

import telescopes


def _get_telescope_location(telescope):
    _latitude, _longitude = telescope.get_location()

    _latitude_deg = _latitude[0] + (_latitude[1] / 60.0) + (
        _latitude[2] / (60.0 * 60.0))
    if _latitude[3] > 0:
        _latitude_deg *= -1.0

    _longitude_deg = _longitude[0] + (_longitude[1] / 60.0) + (
        _longitude[2] / (60.0 * 60.0))
    if _longitude[3] > 0:
        _longitude_deg *= -1.0

    telescope_location = EarthLocation(lat=_latitude_deg * u.deg,
                                       lon=_longitude_deg * u.deg)
    return telescope_location


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d",
                       help="Port telescope is connected to."
                            "Default = /dev/ttyUSB0")
    group.add_argument("--get_azalt", action="store_true")
    group.add_argument("--get_azalt_info", action="store_true")
    group.add_argument("--get_az_alt", action="store_true")
    group.add_argument("--move_az", nargs=1, metavar="new_az")
    group.add_argument("--move_alt", nargs = 1,  metavar="new_alt")
    group.add_argument("--get_location", action="store_true")
    group.add_argument("--get_earth_location", action="store_true")
    group.add_argument("--get_model", action="store_true")
    group.add_argument("--get_radec", action="store_true")
    group.add_argument("--get_ra_dec", action="store_true")
    group.add_argument("--get_time", action="store_true")
    group.add_argument("--get_tracking_mode", action="store_true")
    group.add_argument("--get_version", action="store_true")
    group.add_argument("--set_location", nargs=2,
                       metavar=("latitude", "longitude"))
    group.add_argument("--goto_az_alt", nargs=2, metavar=("az", "alt"))
    group.add_argument("--goto_in_progress", action="store_true")
    group.add_argument("--goto_radec", nargs=2, metavar=("Ra", "Dec"))
    group.add_argument("--set_tracking_mode", metavar="tracking_mode")
    group.add_argument("--set_time")
    group.add_argument("--cancel_goto", action="store_true")
    group.add_argument("--cancel_current_operation", action="store_true")
    group.add_argument("--alignment_complete", action="store_true")
    group.add_argument("--echo")
    group.add_argument("--slew_fixed", nargs=2, metavar=("az_rate", "el_rate"))
    group.add_argument("--slew_var", nargs=2, metavar=("az_rate", "el_rate"))
    group.add_argument("--sync", nargs=2, metavar=("ra", "dec"))

    args = parser.parse_args()

    if args.d:
        device = args.d
    else:
        device = '/dev/ttyUSB0'

    telescope = telescopes.NexStarSLT130(device)

    if args.get_ra_dec:
        print (telescope.get_ra_dec())
    elif args.get_azalt_info:
        _altaz = telescope.get_azalt()
        print(_altaz)
    elif args.get_azalt:
        _altaz = telescope.get_azalt()
        print("alt: " +telescope.dec_to_degrees(_altaz.alt.deg))
        print(" az: " +telescope.dec_to_degrees(_altaz.az.deg))
    elif args.get_az_alt:
        print (telescope.get_az_alt())
    elif args.get_location:
        _earth_location = telescope.get_earth_location()
        print(" lat: "+telescope.dec_to_degrees(_earth_location.latitude.deg))
        print("long: "+telescope.dec_to_degrees(_earth_location.longitude.deg))
    elif args.get_earth_location:
        print telescope.get_earth_location()
    elif args.get_radec:
        _altaz = telescope.get_azalt()
        _radec = _altaz.transform_to('icrs')
        print " ra:" + str(_radec.ra.hms)
        print "dec: " + str(_radec.dec.deg)
    elif args.get_tracking_mode:
        print(telescope.get_tracking_mode())
    elif args.get_version:
        print(telescope.get_version())
    elif args.get_time:
        print(telescope.get_time())
    elif args.set_location:
        latitude = args.set_location[0]
        longitude = args.set_location[1]
        telescope.set_location(
            map(int, longitude.split(",")),
            map(int, latitude.split(","))
        )
    elif args.set_time:
        print "broken!!!!!"
        #telescope.set_time_initializer(map(int, args.set_time_initializer.split(",")))
    elif args.set_tracking_mode:
        telescope.set_tracking_mode(int(args.set_tracking_mode))
    elif args.goto_az_alt:
        _alt = float(args.goto_az_alt[0])
        _az = float(args.goto_az_alt[1])
        telescope.goto_az_alt(_az, _alt)
    elif args.goto_in_progress:
        if telescope.goto_in_progress():
            print("Yes")
        else:
            print("No")
    elif args.goto_radec:
        _ra = float(args.goto_radec[0])
        _dec = float(args.goto_radec[1])
        telescope.goto_radec(_ra, _dec)
    elif args.alignment_complete:
        if telescope.alignment_complete():
            print("Yes")
        else:
            print("No")
    elif args.get_model:
        print telescope.get_model()
    elif args.cancel_goto:
        telescope.cancel_goto()
    elif args.cancel_current_operation:
        telescope.cancel_current_operation()
    elif args.echo:
        telescope.echo(args.echo)
    elif args.slew_fixed:
        _az_rate = float(args.slew_fixed[0])
        _el_rate = float(args.slew_fixed[1])
        telescope.slew_fixed(_az_rate, _el_rate)
    elif args.slew_var:
        _az_rate = float(args.slew_var[0])
        _el_rate = float(args.slew_var[1])
        telescope.slew_var(_az_rate, _el_rate)
    elif args.sync:
        _ra = float(args.sync[0])
        _dec = float(args.sync[1])
        telescope.sync(_ra, _dec)
    elif args.move_alt:
        telescope.move_alt(args.move_alt[0])
    elif args.move_az:
        telescope.move_az(args.move_az[0])

    else:
        print(parser.print_help())


if __name__ == '__main__':
    main()
