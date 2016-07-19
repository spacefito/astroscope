from tests.unit.telescopes.test_base_telescope import TestBaseTelescope
from tests.unit.telescopes.test_nextstart_telescopes import TestNexStarSLT130
from astroscope.telescopes import local_telescopes


class TestNexStarSLT130(TestNexStarSLT130, TestBaseTelescope):
    pass