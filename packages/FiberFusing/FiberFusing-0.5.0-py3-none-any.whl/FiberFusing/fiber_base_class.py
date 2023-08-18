#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from FiberFusing import Circle
from FiberFusing.tools import plot_style
from FiberFusing.axes import Axes
from FiberFusing.utils import get_rho_gradient, get_silica_index
from FiberFusing import OpticalStructure
import pprint

# MPSPlots imports
from MPSPlots import colormaps
from MPSPlots.Render2D import SceneList, Axis, Mesh, Polygon, ColorBar

pp = pprint.PrettyPrinter(indent=4, sort_dicts=False, compact=True, width=1)


class BasedFiber():
    def __init__(self, wavelength: float, position: tuple = (0, 0)):
        self._wavelength = wavelength
        self.position = position
        self.brand = "Unknown"
        self.model = "Unknown"
        self.structure_list = []

    def compute_V_number(self, structure: OpticalStructure) -> float:
        exterior_index = self.structure_list[-1].index

        delta_index = numpy.sqrt(structure.index**2 - exterior_index**2)

        V = 2 * numpy.pi / self.wavelength * delta_index * structure.radius

        return V

    @property
    def pure_silica_index(self):
        return get_silica_index(wavelength=self.wavelength)

    def __str__(self):
        ID = ""

        ID += f"brand: {self.brand:<20s}\n"
        ID += f"model: {self.model:<20s}\n"
        ID += "structure:\n"

        for structure in self.fiber_structure:
            ID += f"\t{structure.name:<20s}"
            ID += f"index: {structure.index:<20.3}"
            ID += f"radius: {structure.radius:<20.3}"
            ID += "\n"

        return ID

    def __repr__(self):
        return self.__str__()


class BaseStructureCollection():
    @property
    def full_structure(self):
        return self.structure_list

    @property
    def fiber_structure(self):
        return [s for s in self.structure_list if s.name not in ['air']]

    @property
    def inner_structure(self):
        return [s for s in self.structure_list if s.name not in ['air', 'outer_clad']]

    @property
    def boundaries(self):
        min_x, min_y, max_x, max_y = [], [], [], []

        for structure in self.fiber_structure:
            boundaries = structure.polygon.bounds

            min_x.append(boundaries[0])
            min_y.append(boundaries[1])
            max_x.append(boundaries[2])
            max_y.append(boundaries[3])

        return (
            numpy.min(min_x),
            numpy.min(min_y),
            numpy.max(max_x),
            numpy.max(max_y)
        )

    def initialize_from_OpticalStructures(self, *optical_structures: OpticalStructure) -> None:
        """
        Initializes structure collection from dictionnary input.

        :param      structure_dictionary:  The structure dictionary
        :type       structure_dictionary:  dict

        :returns:   No returns
        :rtype:     None
        """
        self.add_air()

        for structure in optical_structures:
            self.add_next_structure(structure=structure)

    def add_next_structure(self, structure: dict):
        """
        Add a new circular structure following the previously defined.
        This structure is defined with a name, numerical aperture, and radius.

        :param      name:    The name of the structure
        :type       name:    str
        :param      NA:      The numerical aperture of the structure
        :type       NA:      float
        :param      radius:  The radius of the circular structure
        :type       radius:  float

        :returns:   No returns
        :rtype:     None
        """
        structure.polygon = Circle(position=self.position, radius=structure.radius)

        if structure.from_NA:
            previous_index = self.structure_list[-1].index
            structure.index = self.NA_to_core_index(structure.NA, previous_index)

        setattr(self, structure.name, structure)

        self.structure_list.append(structure)

    def _overlay_structure_on_mesh_(self, structure_list: list, mesh: numpy.ndarray, coordinate_axis: Axis) -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        for structure in structure_list:
            raster = structure.polygon.get_rasterized_mesh(coordinate_axis=coordinate_axis)
            mesh[numpy.where(raster != 0)] = 0

            if structure.from_graded:
                index = self.get_graded_index_mesh(
                    coordinate_axis=coordinate_axis,
                    polygon=structure.polygon,
                    min_index=structure.index,
                    max_index=structure.index + structure.delta_n
                )

            else:
                index = structure.index

            raster *= index

            mesh += raster

        return mesh


class GenericFiber(BasedFiber, BaseStructureCollection):
    def set_position(self, position: tuple):
        for structure in self.structure_list:
            if structure.radius is None:
                continue

            new_polygon = Circle(
                position=position,
                radius=structure.radius,
                index=structure.index
            )

            structure.polygon = new_polygon

    @property
    def wavelength(self):
        if self._wavelength is None:
            raise Exception("Wavelength has not be defined for the fiber.")
        return self._wavelength

    @wavelength.setter
    def wavelength(self, value: tuple):
        self._wavelength = value
        self.__init__()

    def NA_to_core_index(self, NA: float, index_clad: float):
        return numpy.sqrt(NA**2 + index_clad**2)

    def core_index_to_NA(self, interior_index: float, exterior_index: float):
        return numpy.sqrt(interior_index**2 - exterior_index**2)

    @property
    def polygones(self):
        if not self._polygones:
            self.initialize_polygones()
        return self._polygones

    def add_air(self, radius: float = 1e3):
        air_structure = OpticalStructure(
            name='air', 
            from_index=True, 
            index=1, 
            radius=1
        )

        self.add_next_structure(air_structure)

    def add_silica_pure_cladding(self, radius: float = 62.5e-6, name: str = 'outer_clad'):
        clad_structure = OpticalStructure(
            name='outer_clad', 
            from_index=True, 
            index=self.pure_silica_index, 
            radius=radius
        )

        self.add_next_structure(clad_structure)

    def render_patch_on_ax(self, ax: Axis) -> None:
        """
        Add the patch representation of the geometry into the given ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        for structure in self.fiber_structure:
            artist = Polygon(
                instance=structure.polygon._shapely_object
            )

            ax.add_artist(artist)

        ax.set_style(**plot_style.geometry)
        ax.title = 'Fiber structure'

    def render_raster_on_ax(self, ax: Axis, structure, coordinate_axis: Axes) -> None:
        boolean_raster = structure.polygon.get_rasterized_mesh(coordinate_axis=coordinate_axis)

        artist = Mesh(
            x=coordinate_axis.x_vector,
            y=coordinate_axis.y_vector,
            scalar=boolean_raster,
            colormap='Blues'
        )

        ax.add_artist(artist)

    def render_mesh_on_ax(self, ax: Axis, coordinate_axis: Axes):
        """
        Add the rasterized representation of the geometry into the given ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """

        colorbar = ColorBar(
            discreet=False,
            position='right',
            numeric_format='%.4f'
        )

        raster = self.overlay_structures(coordinate_axis=coordinate_axis, structures_type='fiber_structure')

        artist = Mesh(
            x=coordinate_axis.x_vector,
            y=coordinate_axis.y_vector,
            scalar=raster,
            colormap='Blues'
        )

        ax.colorbar = colorbar
        ax.title = 'Rasterized mesh'
        ax.set_style(**plot_style.geometry)
        ax.add_artist(artist)

    def render_gradient_on_ax(self, ax: Axis, coordinate_axis: Axes) -> None:
        """
        Add the rasterized representation of the gradient of the geometrys into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        raster = self.overlay_structures(coordinate_axis=coordinate_axis, structures_type='fiber_structure')

        rho_gradient = get_rho_gradient(mesh=raster, coordinate_axis=coordinate_axis)

        colorbar = ColorBar(
            log_norm=True,
            position='right',
            numeric_format='%.1e',
            symmetric=True
        )

        artist = Mesh(
            x=coordinate_axis.x_vector,
            y=coordinate_axis.y_vector,
            scalar=rho_gradient,
            colormap=colormaps.blue_white_red
        )

        ax.colorbar = colorbar
        ax.title = 'Refractive index gradient'
        ax.set_style(**plot_style.geometry)
        ax.add_artist(artist)

    def shift_coordinates(self, coordinate_axis: Axis, x_shift: float, y_shift: float) -> numpy.ndarray:
        """
        Return the same coordinate system but x-y shifted

        :param      coordinates:  The coordinates
        :type       coordinates:  numpy.ndarray
        :param      x_shift:      The x shift
        :type       x_shift:      float
        :param      y_shift:      The y shift
        :type       y_shift:      float

        :returns:   The shifted coordinate
        :rtype:     numpy.ndarray
        """
        shifted_coordinate = coordinate_axis.to_unstructured_coordinate()
        shifted_coordinate[:, 0] -= x_shift
        shifted_coordinate[:, 1] -= y_shift

        return shifted_coordinate

    def get_shifted_distance_mesh(self, coordinate_axis: Axis, x_position: float, y_position: float, into_mesh: bool = True) -> numpy.ndarray:
        """
        Returns a mesh representing the distance from a specific point.

        :param      coordinate_axis:  The coordinate axis
        :type       coordinate_axis:  Axis
        :param      x_postition:      The x shift
        :type       x_position:       float
        :param      y_position:       The y shift
        :type       y_position:       float
        :param      into_mesh:        Into mesh
        :type       into_mesh:        bool

        :returns:   The shifted distance mesh.
        :rtype:     { return_type_description }
        """
        shifted_coordinate = self.shift_coordinates(
            coordinate_axis=coordinate_axis,
            x_shift=x_position,
            y_shift=y_position
        )

        distance = numpy.sqrt(shifted_coordinate[:, 0]**2 + shifted_coordinate[:, 1]**2)

        if into_mesh:
            distance = distance.reshape(coordinate_axis.shape)

        return distance

    def get_graded_index_mesh(self, coordinate_axis: numpy.ndarray, polygon, min_index: float, max_index: float) -> numpy.ndarray:
        """
        Gets the graded index mesh.
        
        :param      coordinate_axis:  The coordinate axis
        :type       coordinate_axis:  numpy.ndarray
        :param      polygon:          The polygon
        :type       polygon:          Polygon object
        :param      min_index:        The minimum index value for the graded mesh
        :type       min_index:        float
        :param      max_index:        The maximum index value for the graded mesh
        :type       max_index:        float
        
        :returns:   The graded index mesh.
        :rtype:     numpy.ndarray
        """
        shifted_distance_mesh = self.get_shifted_distance_mesh(
            coordinate_axis=coordinate_axis,
            x_position=polygon.center.x,
            y_position=polygon.center.y,
            into_mesh=True
        )

        boolean_raster = polygon.get_rasterized_mesh(coordinate_axis=coordinate_axis)

        shifted_distance_mesh = -boolean_raster * shifted_distance_mesh**2

        shifted_distance_mesh -= shifted_distance_mesh.min()

        normalized_distance_mesh = shifted_distance_mesh / shifted_distance_mesh.max()

        delta_n = max_index - min_index

        normalized_distance_mesh *= delta_n
        normalized_distance_mesh += min_index

        return normalized_distance_mesh

    def overlay_structures(self, coordinate_axis: Axis, structures_type: str = 'inner_structure') -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        mesh = numpy.zeros(coordinate_axis.shape)

        return self.overlay_structures_on_mesh(
            mesh=mesh,
            coordinate_axis=coordinate_axis,
            structures_type=structures_type
        )

    def overlay_structures_on_mesh(self, mesh: numpy.ndarray, coordinate_axis: Axis, structures_type: str = 'inner_structure') -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        return self._overlay_structure_on_mesh_(
            structure_list=getattr(self, structures_type),
            mesh=mesh,
            coordinate_axis=coordinate_axis
        )

    def plot(self, resolution: int = 300) -> None:
        """
        Plot the different representations [patch, raster-mesh, raster-gradient]
        of the geometry.

        :param      resolution:  The resolution to raster the structures
        :type       resolution:  int
        """
        min_x, min_y, max_x, max_y = self.get_structure_max_min_boundaries()

        coordinate_axis = Axes(
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
            nx=resolution,
            ny=resolution
        )

        coordinate_axis.add_padding(padding_factor=1.2)

        figure = SceneList(unit_size=(4, 4), tight_layout=True, ax_orientation='horizontal')

        ax0 = figure.append_ax()
        ax1 = figure.append_ax()
        ax2 = figure.append_ax()

        self.render_patch_on_ax(ax=ax0)
        self.render_mesh_on_ax(ax=ax1, coordinate_axis=coordinate_axis)
        self.render_gradient_on_ax(ax=ax2, coordinate_axis=coordinate_axis)

        return figure

    def get_structures_boundaries(self) -> numpy.ndarray:
        """
        Returns array representing the boundaries of each of the existing structures

        :returns:   The structures boundaries.
        :rtype:     numpy.ndarray
        """
        boundaries = []
        for structure in self.structure_list:
            if structure.name == 'air':
                continue

            boundaries.append(structure.polygon.bounds)

        boundaries = numpy.array(boundaries)

        return boundaries

    def get_structure_max_min_boundaries(self) -> numpy.ndarray:
        """
        Returns array representing max and min x and y [4 points] boundaries
        of the total structures except for air.

        :returns:   The structures max/min boundaries.
        :rtype:     numpy.ndarray
        """
        boundaries = self.get_structures_boundaries()

        min_x, min_y, max_x, max_y = boundaries.T

        min_x = min_x.min()
        max_x = max_x.max()
        min_y = min_y.min()
        max_y = max_y.max()

        return min_x, min_y, max_x, max_y

# -
