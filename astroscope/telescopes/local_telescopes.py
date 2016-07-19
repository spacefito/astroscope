from nextstar_telescopes import NexStarSLT130
from astropy_telescope import AstropyTelescope
from astroscope.computers.local import LocalComputer


class NexStarSLT130(LocalComputer, AstropyTelescope, NexStarSLT130):
    pass
