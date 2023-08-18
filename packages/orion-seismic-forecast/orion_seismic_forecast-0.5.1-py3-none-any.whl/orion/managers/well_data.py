# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
well_data.py
-----------------------
"""

from orion.managers import manager_base
from orion.utilities import timestamp_conversion, file_io
import numpy as np
import utm
import os
from orion.managers.manager_base import recursive


class Well(manager_base.ManagerBase):
    """
    A class for managing well information.
    Note: this class can handle constant and time-varying data

    Attributes:
        x (float): Location of the well in the x-direction (m)
        y (float): Location of the well in the y-direction (m)
        z (float): Location of the well in the z-direction (m)
        init_time (float): Time when pumping started (s)
        flow_rate (float): Average well flow rate (m3/s)
        pressure (float): Average well botom-hole pressure (Pa)
        fname (str): Filename for time-series well data
        old_fname (str): Previous filename for time-series data
        epoch (np.ndarray): Time-series well data t-vector
        N (int): Length of time series data
    """

    def set_class_options(self, **kwargs):
        """
        Well manager initialization
        """
        # Set the shorthand name
        self.short_name = 'Well'

        # Scalar data
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.init_time = 0.0
        self.init_time_input = '0.0'
        self.flow_rate = 0.0
        self.pressure = 0.0

        # Time-series data
        self.fname = ''
        self.old_fname = 'old_fname'
        self.N = 1
        self.data_source = ''

        # Etc.
        self.old_drill_path_name = 'old_fname'
        self.drill_path_name = ''
        self.is_monitor_well = 0

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.variable_flow_rate = []
        self.epoch = []
        self.drill_path = np.zeros(0)

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Gui elements
        self.set_visibility_operator()

        # Note: these will point to the class members by name
        self.gui_elements = {}

        self.gui_elements['short_name'] = {'element_type': 'entry', 'label': 'Name', 'position': [0, 0]}

        self.gui_elements['x'] = {'element_type': 'entry', 'label': 'Location', 'position': [1, 0]}
        self.gui_elements['y'] = {'element_type': 'entry', 'position': [1, 1]}
        self.gui_elements['z'] = {'element_type': 'entry', 'position': [1, 2], 'units': '(m)'}

        self.gui_elements['init_time_input'] = {
            'element_type': 'entry',
            'label': 'Pump start time',
            'position': [2, 0],
            'units': timestamp_conversion.time_units,
            'units_span': 10
        }

        self.gui_elements['flow_rate'] = {
            'element_type': 'entry',
            'label': 'Flow rate',
            'position': [3, 0],
            'units': '(m3/s, injection = +)',
            'units_span': 4
        }

        self.gui_elements['fname'] = {
            'element_type': 'entry',
            'command': 'file',
            'label': 'Flow file',
            'position': [4, 0],
            'filetypes': [('csv', '*.csv'), ('hdf5', '*.hdf5'), ('all', '*')]
        }

        self.gui_elements['drill_path_name'] = {
            'element_type': 'entry',
            'label': 'Path file',
            'position': [5, 0],
            'filetypes': [('csv', '*.csv'), ('all', '*')]
        }

        self.gui_elements['is_monitor_well'] = {
            'element_type': 'check',
            'label': 'Monitor Pressure?',
            'position': [6, 0]
        }

        self.gui_elements['data_source'] = {'element_type': 'text', 'position': [7, 0]}

    @recursive
    def process_inputs(self):
        """
        Build the x, y, z, and t axes of the target grid
        """
        self.init_time = timestamp_conversion.convert_timestamp(self.init_time_input)

    def read_injection_file(self, fname):
        """
        Read fluid injection data
        Note: this function currently supports .dat format

        Args:
            fname (str): Name of the wellbore data file
        """
        self.logger.debug(f'Loading well file: {fname}')

        # Check the file format
        if ('.dat' in fname):
            # Load the data
            tmp = np.loadtxt(fname, unpack=True)

            # The flow rate units in the file are liter/min
            # Convert these to m3/min
            self.variable_flow_rate = tmp[6] / 1e3
            self.pressure = tmp[7]

            # Convert timestamps into epoch format
            year, month, day, hour, minute, second = tmp[:6]
            self.epoch = timestamp_conversion.convert_time_arrays(year, month, day, hour, minute, second)
            self.N = len(self.epoch)
            self.init_time = self.epoch[0]
            self.flow_rate = self.variable_flow_rate[0]

        elif ('csv' in fname):
            tmp = file_io.parse_csv(fname)
            if ('flow_rate' in tmp.keys()):
                self.variable_flow_rate = tmp['flow_rate']
            else:
                self.logger.error('Did not file flow_rate column in well data file')

            if ('epoch' in tmp.keys()):
                self.epoch = tmp['epoch']
            else:
                self.logger.error('Did not file epoch column in well data file')

            self.N = len(self.epoch)
            self.init_time = self.epoch[0]
            self.flow_rate = self.variable_flow_rate[0]

        else:
            self.logger.error(f'Unrecognized well file type: {fname}')

    def convert_units(self, grid):
        zone_id, zone_letter = grid.get_zone_id_letter()
        try:
            self.latitude, self.longitude = utm.to_latlon(self.x, self.y, zone_id, zone_letter)
        except utm.error.OutOfRangeError:
            self.latitude = 0.0
            self.longitude = 0.0

    def load_data(self, grid):
        """
        Load any time series data if necessary
        """
        if self.fname:
            if (self.fname != self.old_fname):
                f = os.path.expanduser(self.fname)
                if os.path.isfile(f):
                    self.read_injection_file(f)
                    self.old_fname = self.fname
                else:
                    self.logger.warning(f'Could not find well file: {f}')

        if self.drill_path_name:
            if (self.drill_path_name != self.old_drill_path_name):
                self.drill_path = np.loadtxt(self.drill_path_name, delimiter=',', skiprows=1)
