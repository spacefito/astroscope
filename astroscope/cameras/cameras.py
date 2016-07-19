
class BaseCamera(object):

    _mirror_delay = 0;

    def __init__(self):
        pass

    def capture_image(self):
        pass

    def reset(self):
        pass

    def download_image(self):
        pass

    def set_exposure(self):
        pass

    def set_trigger_delay(self, delay):
        self._mirror_delay = delay
