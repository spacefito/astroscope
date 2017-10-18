# Copyright 2017 Adolfo Duarte.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Author: __author__

import math

class Star():

    def __init__(self, magnitude = 1.0, distance=1000):
        self._magnitude = magnitude
        self._distance = distance

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        self._magnitude = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value

    def calculate_brightness(self, magnitude):
        '''Calculates brigthness in lux = 1 lument per square meter
        :param magnitude: the magnitude of the star
        :return brightness in lux units
        '''
        return 10**(-0.4 * (magnitude +14.2))

    @property
    def brightness(self):
        return self.calculate_brightness(self._magnitude)


    def calculate_luminosity(self,E,r):
        '''Calulates luminosity

        :param E, brightness in lux (lumen/meter**2)
        :param r, distance to object in meters
        :return luminocity in lumens'''
        return (E *(r**2))

    @property
    def luminosity(self):
        return self.calculate_luminosity(self.brightness, self.distance)