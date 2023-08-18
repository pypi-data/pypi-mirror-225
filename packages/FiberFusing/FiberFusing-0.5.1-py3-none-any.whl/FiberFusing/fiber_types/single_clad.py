#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import OpticalStructure, micro


class FiberCoreA(GenericFiber):
    brand = 'FiberCore'
    model = 'PS1250/1500'
    note = "Boron Doped Photosensitive Fiber"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clad = OpticalStructure(
            name='clad', 
            from_index=True, 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        core = OpticalStructure(
            name='core', 
            from_NA=True, 
            NA=0.12, 
            radius=8.8 / 2 * micro, 
        )

        self.initialize_from_OpticalStructures(clad, core)


class FiberCoreB(GenericFiber):
    brand = 'FiberCore'
    model = 'SM1250'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clad = OpticalStructure(
            name='clad', 
            from_index=True, 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        core = OpticalStructure(
            name='core', 
            from_NA=True, 
            NA=0.12, 
            radius=9.0 / 2 * micro, 
        )

        self.initialize_from_OpticalStructures(clad, core)


if __name__ == '__main__':
    fiber = FiberCoreA(position=(0, 0), wavelength=1550e-9)
    fiber.plot().show()

# -
