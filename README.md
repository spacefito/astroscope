# astroscope
Command line tool and libraries which integrate astropy library and telescopes.

The BaseTelescope class provides a foundation for bulding more complicated telescope classes.
The AstropyTelescope contains functions which depend on the astropy library

The command "astropscope" is a reference python script which provides a CLI. 
<i><b>./astropscope -h</b></i> provides help documenation and avialable flags. 

The command "telescope" is a reference python script which provides a similar CLI as "astroscope" with the difference
that it does not make use of the astropy library. Thiscuts down on import time in case when the software is used in low powered hardware.
<i><b>./telescope -h</b></i> provides help documenation and avialable flags. 

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
