#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber


class CustomFiber(GenericFiber):
    def __init__(self, wavelength: float, structure_dictionary: dict, position: tuple = (0, 0)):
        super().__init__(wavelength=wavelength, position=position)

        self.initialize_from_dictionnary(structure_dictionary=structure_dictionary)


# -
