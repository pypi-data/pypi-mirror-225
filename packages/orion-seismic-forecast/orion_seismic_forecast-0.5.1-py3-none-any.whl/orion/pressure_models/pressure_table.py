# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
pressure_table.py
-----------------------
"""

import os
import numpy as np
from scipy import integrate
from orion.pressure_models import pressure_model_base
from orion.utilities import (hdf5_wrapper, table_files, file_io, function_wrappers, other, openIAM_parser,
                             timestamp_conversion, unit_conversion)


class PressureTableModel(pressure_model_base.PressureModelBase):
    """
    Pressure model based off of Theis Solution

    Attributes:
        file_name (string): Table filename
        p_interp (scipy.interpolate.LinearNDInterpolator): pressure interpolator
        dpdt_interp (scipy.interpolate.LinearNDInterpolator): dpdt interpolator

    """

    def set_class_options(self, **kwargs):
        """
        Initialization function

        """
        # Model configuration
        self.short_name = 'Pressure Table'
        self.file_name = ''

        # Table units
        self.available_spatial_units = ['meter', 'kilometer', 'feet', 'mile']
        self.spatial_units = self.available_spatial_units[0]
        self.available_time_units = ['second', 'minute', 'hour', 'day', 'year']
        self.time_units = self.available_time_units[0]
        self.spatial_scale = 1.0
        self.time_scale = 1.0

        # Table offsets
        self.table_offset_x = 0.0
        self.table_offset_y = 0.0
        self.table_offset_z = 0.0
        self.table_offset_t = 0.0
        self.table_offset_t_str = '0'

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        super().set_data(**kwargs)
        self.p_interp = None
        self.dpdt_interp = None
        self.model = None

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Add values to gui
        self.gui_elements['file_name'] = {
            'element_type': 'entry',
            'command': 'file',
            'label': 'File',
            'position': [0, 0],
            'filetypes': [('hdf5', '*.hdf5'), ('zip', '*.zip'), ('csv', '*.csv'), ('all', '*')]
        }
        self.gui_elements['spatial_units'] = {
            'element_type': 'dropdown',
            'label': 'Distance units',
            'position': [1, 0],
            'values': self.available_spatial_units
        }
        self.gui_elements['time_units'] = {
            'element_type': 'dropdown',
            'label': 'Time units',
            'position': [2, 0],
            'values': self.available_time_units
        }
        self.gui_elements['table_offset_x'] = {'element_type': 'entry', 'label': 'Spatial origin', 'position': [3, 0]}
        self.gui_elements['table_offset_y'] = {'element_type': 'entry', 'position': [3, 1]}
        self.gui_elements['table_offset_z'] = {'element_type': 'entry', 'units': '(x, y, z)', 'position': [3, 2]}
        self.gui_elements['table_offset_t_str'] = {'element_type': 'entry', 'label': 'Time origin', 'position': [4, 0]}

    def process_inputs(self):
        """
        Process unit and offset information
        """
        unit_converter = unit_conversion.UnitManager()
        self.spatial_scale = unit_converter(self.spatial_units)
        self.time_scale = unit_converter(self.time_units)

        if '/' in self.table_offset_t_str:
            self.table_offset_t = timestamp_conversion.convert_timestamp(self.table_offset_t_str) / self.time_scale
        else:
            self.table_offset_t = float(self.table_offset_t_str)

    def reset_data(self, grid):
        self.p_interp = function_wrappers.constant_fn(0.0)
        self.dpdt_interp = function_wrappers.constant_fn(0.0)
        self.grid_values(grid)

    def p(self, x, y, z, t):
        return self.p_interp(x, y, z, t + self.t_origin)

    def dpdt(self, x, y, z, t):
        return self.dpdt_interp(x, y, z, t + self.t_origin)

    def run(self, grid, well_manager, geologic_model):
        data = {}
        f = os.path.expanduser(self.file_name)
        if not os.path.isfile(f):
            self.logger.warning(f'Cannot find pressure table file: {f}')
            self.reset_data(grid)
            return

        elif ('hdf5' in f):
            self.logger.debug(f'Loading pressure table from hdf5 file: {f}')
            tmp = hdf5_wrapper.hdf5_wrapper(f)
            data = tmp.get_copy()
            self.parse_structured_table_data(data)
        elif ('csv' in f):
            self.logger.debug(f'Loading pressure table from csv file: {f}')
            data = file_io.parse_csv(f)
            self.parse_structured_table_data(data)
        elif ('zip' in f):
            self.logger.debug(f'Loading OpenIAM table from csv file: {f}')
            self.parse_openIAMModel(f)
        else:
            self.logger.error(f'File format not recognized: {f}')

        self.grid_values(grid)

    def parse_structured_table_data(self, data):
        # Check to see whether we need to calculate pressure or dpdt
        if ('t' not in data):
            raise Exception('The pressure table file is missing t')
        if ('pressure' not in data):
            if ('dpdt' in data):
                data['pressure'] = integrate.cumtrapz(data['dpdt'], data['t'], initial=0.0, axis=-1)
            else:
                raise Exception('The pressure table file requires either pressure or dpdt')
        if ('dpdt' not in data):
            if ('pressure' in data):
                scale_shape = np.ones(len(np.shape(data['pressure'])), dtype=int)
                scale_shape[-1] = -1
                data['dpdt'] = other.derivative(data['pressure'], data['t'], axis=-1)
            else:
                raise Exception('The pressure table file requires either pressure or dpdt')

        interps = table_files.load_table_files(data)
        self.p_interp = interps['pressure']
        self.dpdt_interp = interps['dpdt']

    def parse_openIAMModel(self, fname):
        spatial_offset = np.array([self.table_offset_x, self.table_offset_y, self.table_offset_z])
        model = openIAM_parser.OpenIAMParser(fname,
                                             time_scale=self.time_scale,
                                             time_offset=self.table_offset_t,
                                             spatial_scale=self.spatial_scale,
                                             spatial_offset=spatial_offset)
        properties = list(model.keys())
        if ('pressure' not in properties):
            if ('dpdt' in properties):
                dpdt = np.array(model.properties['dpdt'])
                p = integrate.cumtrapz(dpdt, model.t, initial=0.0, axis=0)
                model.properties['pressure'] = [np.ascontiguousarray(np.squeeze(x)) for x in np.split(p, model.Nt)]
            else:
                raise Exception('The OpenIAM model requires pressure or dpdt')
        if ('dpdt' not in properties):
            if ('pressure' in properties):
                p = np.array(model.properties['pressure'])
                dpdt = other.derivative(p, model.t, axis=0)
                model.properties['dpdt'] = [np.ascontiguousarray(np.squeeze(x)) for x in np.split(dpdt, model.Nt)]
            else:
                raise Exception('The OpenIAM model requires pressure or dpdt')

        self.model = model

        # Handle model dimensions
        if self.model.Ndim == 3:
            mask = [0, 1, 3]
            self.p_interp = function_wrappers.masked_fn(self.model['pressure'], mask)
            self.dpdt_interp = function_wrappers.masked_fn(self.model['dpdt'], mask)
        else:
            self.p_interp = self.model['pressure']
            self.dpdt_interp = self.model['dpdt']
