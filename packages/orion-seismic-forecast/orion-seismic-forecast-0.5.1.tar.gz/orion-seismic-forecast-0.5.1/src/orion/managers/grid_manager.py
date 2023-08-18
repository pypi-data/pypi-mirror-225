# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
grid_manager.py
-----------------------
"""

import numpy as np
from orion.managers import manager_base
from orion.utilities import timestamp_conversion
import utm
from orion.managers.manager_base import recursive


class GridManager(manager_base.ManagerBase):
    """
    Grid manager class

    Attributes:
        ref_time_str (str): Reference time string in dd/mm/yyyy format
        spatial_type (str): Style of spatial inputs (default='UTM')
        t (np.ndarray): Time axis (s)
        t_min (float): Minimum time (s)
        t_max (float): Maximum time (s)
        dt (float): Target time resolution (s)
        x (np.ndarray): X axis (m)
        x_min (float): Minimum X value (m)
        x_max (float): Maximum X value (m)
        dx (float): Target resolution in the X direction (m)
        y (np.ndarray): Y axis (m)
        y_min (float): Minimum Y value (m)
        y_max (float): Maximum Y value (m)
        dy (float): Target resolution in the Y direction (m)
        z (np.ndarray): Z axis (m)
        z_min (float): Minimum Z value (m)
        z_max (float): Maximum Z value (m)
        dz (float): Target resolution in the Z direction (m)
    """

    def set_class_options(self, **kwargs):
        """
        Grid manager initialization
        """

        # Set the shorthand name
        self.short_name = 'General'

        # Time control
        self.time_header = 'Time'
        self.t_origin = 0.0
        self.ref_time_str = '0.0'
        self.t_min = 0.0
        self.t_max = 1.0
        self.dt = 1.0
        self.t_min_input = 0.0
        self.t_max_input = 100.0
        self.dt_input = 50.0
        self.snapshot_time = 0.0

        # Plot extents (local time, days)
        self.plot_time_min = 0.0
        self.plot_time_max = 100.0

        # Spatial control
        self.spatial_header = '\nSpatial'

        self.spatial_labels = {'UTM': '(m)', 'Lat Lon': '(degrees)'}
        self.spatial_axes = {
            'UTM': ['East (m)', 'North (m)'],
            'Lat Lon': [r'Longitude ($\circ$)', r'Latitude ($\circ$)']
        }
        self.available_spatial_types = sorted(self.spatial_labels.keys())
        self.spatial_type = self.available_spatial_types[-1]
        self.current_spatial_type = ''
        self.unit_label = self.spatial_labels[self.spatial_type]

        # Note: The default UTM origin is not (0, 0, 0)
        #        because that is not a valid location for the projection.
        self.x_origin = 542630.0
        self.x_min = 0.0
        self.x_max = 1000.0
        self.dx = 1000.0
        self.y_origin = 4184197.0
        self.y_min = 0.0
        self.y_max = 1000.0
        self.dy = 1000.0
        self.z_origin = 0.0
        self.z_min = 0.0
        self.z_max = 100.0
        self.dz = 100.0

        # Projection
        self.utm_zone = '10S'
        self.projection = "+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m"

        # Flag to allow pressure models to modify the grid
        self.allow_grid_modification = 0

        # Flag to avoid precision issues with coordinate conversion
        self.round_conversion = True

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.style_record = {k: {} for k in self.available_spatial_types}
        self.t = np.zeros(0)
        self.x = np.zeros(0)
        self.y = np.zeros(0)
        self.z = np.zeros(0)
        self.areas = np.zeros((2, 2))
        self.latitude = np.zeros(0)
        self.longitude = np.zeros(0)

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_operator()

        # Add gui elements
        self.gui_elements['time_header'] = {'element_type': 'text', 'position': [0, 0]}
        self.gui_elements['ref_time_str'] = {
            'element_type': 'entry',
            'label': 'Reference Time',
            'position': [1, 0],
            'units': timestamp_conversion.time_units,
            'units_span': 10
        }

        self.gui_elements['t_min_input'] = {'element_type': 'entry', 'label': 'Time Range:  min', 'position': [2, 0]}
        self.gui_elements['t_max_input'] = {'element_type': 'entry', 'label': 'max', 'position': [2, 1]}
        self.gui_elements['dt_input'] = {
            'element_type': 'entry',
            'label': 'dt',
            'position': [2, 2],
            'units': '(days)',
            'units_span': 4
        }

        self.gui_elements['plot_time_min'] = {'element_type': 'entry', 'label': 'Plot time:  min', 'position': [3, 0]}
        self.gui_elements['plot_time_max'] = {
            'element_type': 'entry',
            'label': 'max',
            'position': [3, 1],
            'units': '(days)',
            'units_span': 4
        }

        # Spatial
        self.gui_elements['spatial_header'] = {'element_type': 'text', 'position': [4, 0]}
        self.gui_elements['spatial_type'] = {
            'element_type': 'dropdown',
            'label': 'Spatial style',
            'position': [5, 0],
            'values': self.available_spatial_types,
            'command': self.switch_style,
            'pre_update': 'frame',
            'post_update': 'frame'
        }

        self.gui_elements['utm_zone'] = {'element_type': 'entry', 'label': 'zone', 'position': [5, 1]}

        self.gui_elements['x_origin'] = {'element_type': 'entry', 'label': 'Origin:     x', 'position': [6, 0]}
        self.gui_elements['y_origin'] = {'element_type': 'entry', 'label': 'y', 'position': [6, 1]}
        self.gui_elements['z_origin'] = {'element_type': 'entry', 'label': 'z', 'position': [6, 2]}

        self.gui_elements['x_min'] = {'element_type': 'entry', 'label': 'X Range:  min', 'position': [7, 0]}
        self.gui_elements['x_max'] = {'element_type': 'entry', 'label': 'max', 'position': [7, 1]}
        self.gui_elements['dx'] = {'element_type': 'entry', 'label': 'dx', 'position': [7, 2]}

        self.gui_elements['y_min'] = {'element_type': 'entry', 'label': 'Y Range:  min', 'position': [8, 0]}
        self.gui_elements['y_max'] = {'element_type': 'entry', 'label': 'max', 'position': [8, 1]}
        self.gui_elements['dy'] = {'element_type': 'entry', 'label': 'dy', 'position': [8, 2]}

        self.gui_elements['z_min'] = {'element_type': 'entry', 'label': 'Z Range:  min', 'position': [9, 0]}
        self.gui_elements['z_max'] = {'element_type': 'entry', 'label': 'max', 'position': [9, 1]}
        self.gui_elements['dz'] = {'element_type': 'entry', 'label': 'dz', 'position': [9, 2]}

        self.gui_elements['unit_label'] = {'element_type': 'text', 'position': [[6, 3], [7, 3], [8, 3], [9, 3]]}

        self.gui_elements['allow_grid_modification'] = {
            'element_type': 'check',
            'label': 'Permit modification',
            'position': [10, 0]
        }
        self.gui_elements['round_conversion'] = {'element_type': 'check', 'label': 'Round', 'position': [10, 1]}

    @recursive
    def process_inputs(self):
        """
        Build the x, y, z, and t axes of the target grid
        """
        self.logger.debug('Setting up the grid')
        self.t_origin = timestamp_conversion.convert_timestamp(self.ref_time_str)

        # Convert t inputs from days to seconds
        t_scale = 60.0 * 60.0 * 24.0
        self.t_min = self.t_min_input * t_scale
        self.t_max = self.t_max_input * t_scale
        self.dt = self.dt_input * t_scale

        # Setup grid values
        Nt = max(int(np.ceil((self.t_max - self.t_min) / self.dt)), 2)
        Nx = max(int(np.ceil((self.x_max - self.x_min) / self.dx)), 2)
        Ny = max(int(np.ceil((self.y_max - self.y_min) / self.dy)), 2)
        Nz = max(int(np.ceil((self.z_max - self.z_min) / self.dz)), 2)

        # Setup grids
        if not self.current_spatial_type:
            self.current_spatial_type = self.spatial_type

        if (self.spatial_type == 'UTM'):
            self.process_utm()
        else:
            self.process_latlon()

        # Update the projection
        self.projection = f"+proj=eqc +lat_ts=0 +lat_0={self.style_record['Lat Lon']['origin'][1]:1.5f} +lon_0={self.style_record['Lat Lon']['origin'][0]:1.5f} +ellps=WGS84 +units=m"

        # Setup grid
        self.t = np.linspace(self.t_min, self.t_max, Nt)
        self.x = np.linspace(self.style_record['UTM']['corner_a'][0], self.style_record['UTM']['corner_b'][0], Nx)
        self.y = np.linspace(self.style_record['UTM']['corner_a'][1], self.style_record['UTM']['corner_b'][1], Ny)
        self.z = np.linspace(self.z_min, self.z_max, Nz) + self.z_origin
        self.latitude = np.linspace(self.style_record['Lat Lon']['corner_a'][1],
                                    self.style_record['Lat Lon']['corner_b'][1], Nx)
        self.longitude = np.linspace(self.style_record['Lat Lon']['corner_a'][0],
                                     self.style_record['Lat Lon']['corner_b'][0], Ny)

        # Calculate grid areas
        dx = np.diff(self.x)
        dx = np.append(dx, dx[-1:], axis=0)
        dy = np.diff(self.y)
        dy = np.append(dy, dy[-1:], axis=0)
        self.areas = np.outer(dx, dy)

    def process_utm(self):
        self.style_record['UTM']['origin'] = [self.x_origin, self.y_origin]
        self.style_record['UTM']['corner_a'] = [self.x_min + self.x_origin, self.y_min + self.y_origin]
        self.style_record['UTM']['corner_b'] = [self.x_max + self.x_origin, self.y_max + self.y_origin]
        self.style_record['UTM']['dx'] = [self.dx, self.dy]

        zone_id = int(self.utm_zone[:-1])
        zone_letter = self.utm_zone[-1]
        try:
            self.style_record['Lat Lon']['origin'] = utm.to_latlon(self.x_origin, self.y_origin, zone_id,
                                                                   zone_letter)[::-1]
            self.style_record['Lat Lon']['corner_a'] = utm.to_latlon(self.x_min + self.x_origin,
                                                                     self.y_min + self.y_origin, zone_id,
                                                                     zone_letter)[::-1]
            self.style_record['Lat Lon']['corner_b'] = utm.to_latlon(self.x_max + self.x_origin,
                                                                     self.y_max + self.y_origin, zone_id,
                                                                     zone_letter)[::-1]
            Nx = int(np.ceil((self.x_max - self.x_min) / self.dx))
            Ny = int(np.ceil((self.y_max - self.y_min) / self.dy))
            self.style_record['Lat Lon']['dx'] = [
                (self.style_record['Lat Lon']['corner_b'][0] - self.style_record['Lat Lon']['corner_a'][0]) / Nx,
                (self.style_record['Lat Lon']['corner_b'][1] - self.style_record['Lat Lon']['corner_a'][1]) / Ny
            ]
        except utm.error.OutOfRangeError:
            self.logger.warning('Grid UTM values out of range... This may be a local coordinate system.')
            self.style_record['Lat Lon']['origin'] = [0.0, 0.0]
            self.style_record['Lat Lon']['corner_a'] = [0.0, 0.0]
            self.style_record['Lat Lon']['corner_b'] = [1.0, 1.0]
            Nx = int(np.ceil((self.x_max - self.x_min) / self.dx))
            Ny = int(np.ceil((self.y_max - self.y_min) / self.dy))
            self.style_record['Lat Lon']['dx'] = [1.0 / Nx, 1.0 / Ny]

    def process_latlon(self):
        self.style_record['Lat Lon']['origin'] = [self.x_origin, self.y_origin]
        self.style_record['Lat Lon']['corner_a'] = [self.x_min + self.x_origin, self.y_min + self.y_origin]
        self.style_record['Lat Lon']['corner_b'] = [self.x_max + self.x_origin, self.y_max + self.y_origin]
        self.style_record['Lat Lon']['dx'] = [self.dx, self.dy]

        self.style_record['UTM']['origin'] = list(utm.from_latlon(self.y_origin, self.x_origin))
        self.utm_zone = str(self.style_record['UTM']['origin'][2]) + self.style_record['UTM']['origin'][3]
        self.style_record['UTM']['corner_a'] = list(
            utm.from_latlon(self.y_min + self.y_origin, self.x_min + self.x_origin))
        self.style_record['UTM']['corner_b'] = list(
            utm.from_latlon(self.y_max + self.y_origin, self.x_max + self.x_origin))

        if (self.round_conversion):
            for k in ['origin', 'corner_a', 'corner_b']:
                for ii in [0, 1]:
                    self.style_record['UTM'][k][ii] = np.round(self.style_record['UTM'][k][ii])

        Nx = int(np.ceil((self.x_max - self.x_min) / self.dx))
        Ny = int(np.ceil((self.y_max - self.y_min) / self.dy))
        self.style_record['UTM']['dx'] = [
            (self.style_record['UTM']['corner_b'][0] - self.style_record['UTM']['corner_a'][0]) / Nx,
            (self.style_record['UTM']['corner_b'][1] - self.style_record['UTM']['corner_a'][1]) / Ny
        ]

    def switch_style(self):
        if self.current_spatial_type == self.spatial_type:
            return

        self.unit_label = self.spatial_labels[self.spatial_type]
        if (self.spatial_type == 'UTM'):
            self.process_latlon()
        else:
            self.process_utm()
        self.x_origin = self.style_record[self.spatial_type]['origin'][0]
        self.x_min = self.style_record[self.spatial_type]['corner_a'][0] - self.x_origin
        self.x_max = self.style_record[self.spatial_type]['corner_b'][0] - self.x_origin
        self.dx = self.style_record[self.spatial_type]['dx'][0]
        self.y_origin = self.style_record[self.spatial_type]['origin'][1]
        self.y_min = self.style_record[self.spatial_type]['corner_a'][1] - self.y_origin
        self.y_max = self.style_record[self.spatial_type]['corner_b'][1] - self.y_origin
        self.dy = self.style_record[self.spatial_type]['dx'][1]
        self.current_spatial_type = self.spatial_type

    def get_axes_labels(self):
        return self.spatial_axes[self.spatial_type]

    def get_lat_lon_box(self):
        return self.style_record['Lat Lon']['corner_a'], self.style_record['Lat Lon']['corner_b']

    def get_zone_id_letter(self):
        if self.utm_zone:
            zone_id = int(self.utm_zone[:-1])
            zone_letter = self.utm_zone[-1]
            return zone_id, zone_letter
        else:
            self.logger.warning('No utm zone information available')
            return 1, 'S'

    def get_plot_range(self):
        x_range = []
        y_range = []
        if (self.spatial_type == 'UTM'):
            x_range = [self.x_min, self.x_max]
            y_range = [self.y_min, self.y_max]
            # x_range = [self.x_min + self.x_origin, self.x_max + self.x_origin]
            # y_range = [self.y_min + self.y_origin, self.y_max + self.y_origin]
        else:
            x_range = [self.x_min + self.x_origin, self.x_max + self.x_origin]
            y_range = [self.y_min + self.y_origin, self.y_max + self.y_origin]
        return x_range, y_range

    def get_plot_data(self, projection):
        plot_data = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            't': self.t,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'x_origin': self.x_origin,
            'y_origin': self.y_origin,
            'z_origin': self.z_origin,
            't_origin': self.t_origin,
            'snapshot_time': self.snapshot_time
        }
        return plot_data

    def check_grid(self, new_grid):
        if self.allow_grid_modification:
            self.logger.debug('Modifying the grid dimensions')
            if ('x' in new_grid):
                self.x = new_grid['x']
                self.x_min = self.x[0] - self.x_origin
                self.x_max = self.x[-1] - self.x_origin
                self.dx = (self.x_max - self.x_min) / len(self.x)
            else:
                self.dx = self.x_max - self.x_min
                self.x = self.x[:1]

            if ('y' in new_grid):
                self.y = new_grid['y']
                self.y_min = self.y[0] - self.y_origin
                self.y_max = self.y[-1] - self.y_origin
                self.dy = (self.y_max - self.y_min) / len(self.y)
            else:
                self.dy = self.y_max - self.y_min
                self.y = self.y[:1]

            if ('z' in new_grid):
                self.z = new_grid['z']
                self.z_min = self.z[0] - self.z_origin
                self.z_max = self.z[-1] - self.z_origin
                self.dz = (self.z_max - self.z_min) / len(self.z)
            else:
                self.dz = self.z_max - self.z_min
                self.z = self.z[:1]

            if ('t' in new_grid):
                self.t = new_grid['t'] - self.t_origin
                self.t_min = self.t[0]
                self.t_max = self.t[-1]
                self.dt = (self.t_max - self.t_min) / len(self.t)
            else:
                self.dt = self.t[-1] - self.t[0]
                self.t = self.t[:1]

            # Update input values for time
            t_scale = 60.0 * 60.0 * 24.0
            self.t_min_input = self.t_min / t_scale
            self.t_max_input = self.t_max / t_scale
            self.dt_input = self.dt / t_scale

    def get_digitize_axes(self, N):
        grid_order = []
        if (N == 1):
            grid_order = [self.t]
        elif (N == 3):
            grid_order = [self.x, self.y, self.z]
        elif (N == 4):
            grid_order = [self.x, self.y, self.z, self.t]
        else:
            raise Exception('Unrecognized number of dimensions for grid digitization')
        return grid_order

    def digitize_values(self, *args, include_edges=False):
        """
        Find the bin IDs for a set of points

        Args:
            args (list): List of points to digitize (1=t, 3=xyz, 4=xyzt)

        Returns:
            list: list of 1D arrays containing grid indices
        """
        grid_order = self.get_digitize_axes(len(args))

        grid_id = []
        for ii, axis in enumerate(grid_order):
            M = len(axis)
            if (M > 1):
                bins = 0.5 * (axis[1:] + axis[:-1])
                da = 0.5 * (axis[1] - axis[0])
                bins = np.concatenate([[axis[0] - da], bins, [axis[-1] + da]], axis=0)
                tmp = np.digitize(args[ii], bins) - 1
                if include_edges:
                    grid_id.append(np.maximum(np.minimum(tmp, M - 1), 0))
                else:
                    tmp[tmp < 0] = np.NaN
                    tmp[tmp >= M] = np.NaN
                    grid_id.append(tmp)
        return grid_id

    def histogram_values(self, *args, include_edges=False):
        """
        Calculate the histogram for a set of points

        Args:
            args (list): List of points to calculate histogram (1=t, 3=xyz, 4=xyzt)

        Returns:
            np.ndarray: ND histogram of points
        """
        grid_id = self.digitize_values(*args, include_edges=include_edges)
        if not include_edges:
            Ia = np.all(~np.isnan(grid_id), axis=0)
            for ii in len(args):
                grid_id[ii] = grid_id[ii][Ia]

        grid_order = self.get_digitize_axes(len(args))
        count = np.zeros([len(x) for x in grid_order], dtype=int)
        np.add.at(count, tuple(grid_id), 1)
        return count

    @property
    def shape(self):
        """
        Get the shape of the grid
        """
        return (len(self.x), len(self.y), len(self.z), len(self.t))
