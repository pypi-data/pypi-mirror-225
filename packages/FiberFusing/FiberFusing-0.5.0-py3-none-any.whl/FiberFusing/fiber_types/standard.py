#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import OpticalStructure, micro


class SMF28(GenericFiber):
    brand = 'Corning'
    model = "SMF28"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clad = OpticalStructure(
            name='outer_clad', 
            from_index=True, 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        core = OpticalStructure(
            name='core', 
            from_NA=True, 
            NA=0.12, 
            radius=8.2 / 2 * micro, 
        )

        self.initialize_from_OpticalStructures(clad, core)


class HP630(GenericFiber):
    brand = 'Thorlab'
    model = "HP630"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clad = OpticalStructure(
            name='outer_clad', 
            from_index=True, 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        core = OpticalStructure(
            name='core', 
            from_NA=True, 
            NA=0.13, 
            radius=3.5 / 2 * micro, 
        )

        self.initialize_from_OpticalStructures(clad, core)


class HI1060(GenericFiber):
    brand = 'Corning'
    model = "HI630"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clad = OpticalStructure(
            name='outer_clad', 
            from_index=True, 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        core = OpticalStructure(
            name='core', 
            from_NA=True, 
            NA=0.14, 
            radius=5.3 / 2 * micro, 
        )

        self.initialize_from_OpticalStructures(clad, core)


if __name__ == '__main__':
    fiber = SMF28(position=(0, 0), wavelength=1550e-9)
    fiber.plot().show()

# -
