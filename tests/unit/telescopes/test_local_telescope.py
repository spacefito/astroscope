from tests.unit.telescopes.test_base_telescope import TestBaseTelescope
from astroscope.telescopes import local_telescopes


class TestNexStarSLT130(TestBaseTelescope):

    def setUp(self):
        self.serial_device = "fake_device"
        self.telescope = local_telescopes.NexStarSLT130(self.serial_device)

