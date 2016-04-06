# astroscope
Command line tool and libraries which integrate astropy library and telescopes.
The command "astropscope" is a reference python script which provides a command interface to the libraries. 
<i><b>./astropscope -h</b></i> provides help documenation and avialable flags. 

The BaseTelescope class is the class which implements the astropy based telescope. BaseTelescope should
contain the higher level algorithms which use astropy to do astronomomical calculations and other higher level computations. 
BaseTelescope contains a few "abstract" methods which should be implemented by any particular telesope interface to be able to control
a real telescope. The example included is based on a Celestron SLT 130 telescope from Celestron. The class is called NexStarSLT130,
and it provides an interface to connect to the telescope via the NexStar+ handhel controller. The default connection is /dev/ttyUSB0.

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
