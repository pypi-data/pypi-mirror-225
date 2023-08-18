# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
geologic_model_manager.py
---------------------------
"""

import os
import numpy as np
from orion.managers import manager_base
from orion.utilities import hdf5_wrapper, function_wrappers, table_files, plot_tools
from orion.utilities.plot_config import gui_colors


class GeologicModelManager(manager_base.ManagerBase):
    """
    A class for managing the geologic model
    methods within ORION

    Attributes:
        available_models (list): A comprehensive list of available forecast models
        permeability (scipy.interpolate.LinearNDInterpolator): Permeability interpolation function (3D)
        permeability_uniform (float): Value for a uniform permeability field
        permeability_file (float): Filename containing structured/unstructured permeability values and grid/locations
        sigma_xx (scipy.interpolate.LinearNDInterpolator): stress interpolation function (xx component, 3D)
        sigma_yy (scipy.interpolate.LinearNDInterpolator): stress interpolation function (yy component, 3D)
        sigma_zz (scipy.interpolate.LinearNDInterpolator): stress interpolation function (zz component, 3D)
        sigma_xy (scipy.interpolate.LinearNDInterpolator): stress interpolation function (xy component, 3D)
        sigma_xz (scipy.interpolate.LinearNDInterpolator): stress interpolation function (xz component, 3D)
        sigma_yz (scipy.interpolate.LinearNDInterpolator): stress interpolation function (yz component, 3D)
        sigma_xx_uniform (float): Value for a uniform stress field (xx component)
        sigma_yy_uniform (float): Value for a uniform stress field (yy component)
        sigma_zz_uniform (float): Value for a uniform stress field (zz component)
        sigma_xy_uniform (float): Value for a uniform stress field (xy component)
        sigma_xz_uniform (float): Value for a uniform stress field (xz component)
        sigma_yz_uniform (float): Value for a uniform stress field (yz component)
        sigma_file (float): Filename containing structured/unstructured stress values and grid/locations

    """

    def set_class_options(self, **kwargs):
        """
        Geologic model manager initialization

        """
        # Set the shorthand name
        self.short_name = 'Geologic Model'

        # Fluid flow
        self.permeability_uniform = 1.0
        self.permeability_file = ''

        # Stress
        self.sigma_xx_uniform = 0.0
        self.sigma_yy_uniform = 0.0
        self.sigma_zz_uniform = 0.0
        self.sigma_xy_uniform = 0.0
        self.sigma_xz_uniform = 0.0
        self.sigma_yz_uniform = 0.0
        self.sigma_file = ''

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.permeability = np.zeros(0)
        self.sigma_xx = np.zeros(0)
        self.sigma_yy = np.zeros(0)
        self.sigma_zz = np.zeros(0)
        self.sigma_xy = np.zeros(0)
        self.sigma_xz = np.zeros(0)
        self.sigma_yz = np.zeros(0)

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.show_plots = False

        # Figures
        # self.figures['permeability'] = {
        #     'position': [0, 0],
        #     'layer_config': True,
        #     'size': (7, 6),
        #     'extra_axis_size': (1.1, 2),
        #     'target': 'empty_plot'
        # }

        # Gui elements
        # Note: these will point to the class members by name
        self.gui_elements = {}

        self.gui_elements['permeability_uniform'] = {
            'element_type': 'entry',
            'label': 'Permeability (uniform)',
            'position': [0, 0],
            'units': 'mD'
        }
        self.gui_elements['permeability_file'] = {
            'element_type': 'entry',
            'command': 'file',
            'label': 'Permeability (heterogeneous)',
            'position': [1, 0],
            'filetypes': [('hdf5', '*.hdf5'), ('csv', '*.csv'), ('all', '*')]
        }

        self.gui_elements['sigma_xx_uniform'] = {
            'element_type': 'entry',
            'label': 'Stress Tensor (uniform)  sxx',
            'position': [2, 0]
        }
        self.gui_elements['sigma_xy_uniform'] = {'element_type': 'entry', 'label': 'sxy', 'position': [2, 1]}
        self.gui_elements['sigma_xz_uniform'] = {'element_type': 'entry', 'label': 'sxz', 'position': [2, 2]}
        self.gui_elements['sigma_yy_uniform'] = {'element_type': 'entry', 'label': 'syy', 'position': [3, 1]}
        self.gui_elements['sigma_yz_uniform'] = {'element_type': 'entry', 'label': 'syz', 'position': [3, 2]}
        self.gui_elements['sigma_zz_uniform'] = {
            'element_type': 'entry',
            'label': 'szz',
            'position': [4, 2],
            'units': 'MPa'
        }

        self.gui_elements['sigma_file'] = {
            'element_type': 'entry',
            'label': 'Stress (heterogeneous)',
            'position': [5, 0],
            'filetypes': [('hdf5', '*.hdf5'), ('csv', '*.csv'), ('all', '*')]
        }

    def load_data(self, grid):
        """
        Load permeability and stress data from a file
        """
        # Load permeability estimates
        f = os.path.expanduser(self.permeability_file)
        if os.path.isfile(f):
            self.logger.debug('Loading permeability data from hdf5 file')
            tmp = hdf5_wrapper.hdf5_wrapper(self.permeability_file)
            data = tmp.get_copy()
            self.permeability = table_files.load_table_files(data)['permeability']
        else:
            if f:
                self.logger.warning(f'Could not find permeability file: {f}')
            self.logger.debug(f'Using constant permeability: {self.permeability_uniform:1.4e}')
            self.permeability = function_wrappers.constant_fn(self.permeability_uniform)

        # Load in-situ stress estimates
        self.logger.debug('Loading stress data')
        f = os.path.expanduser(self.sigma_file)
        if os.path.isfile(f):
            tmp = hdf5_wrapper.hdf5_wrapper(self.sigma_file)
            data = tmp.get_copy()
            stress_interps = table_files.load_table_files(data)
            self.sigma_xx = stress_interps['sigma_xx']
            self.sigma_yy = stress_interps['sigma_yy']
            self.sigma_zz = stress_interps['sigma_zz']
            self.sigma_xy = stress_interps['sigma_xy']
            self.sigma_xz = stress_interps['sigma_xz']
            self.sigma_yz = stress_interps['sigma_yz']
        else:
            if f:
                self.logger.warning(f'Could not find stress file: {f}')
            stress_ordered = (self.sigma_xx_uniform, self.sigma_yy_uniform, self.sigma_zz_uniform,
                              self.sigma_xy_uniform, self.sigma_xz_uniform, self.sigma_yz_uniform)
            self.logger.debug(f'Using constant stress: [{", ".join(f"{x:1.4e}" for x in stress_ordered)}]')
            self.sigma_xx = function_wrappers.constant_fn(self.sigma_xx_uniform)
            self.sigma_yy = function_wrappers.constant_fn(self.sigma_yy_uniform)
            self.sigma_zz = function_wrappers.constant_fn(self.sigma_zz_uniform)
            self.sigma_xy = function_wrappers.constant_fn(self.sigma_xy_uniform)
            self.sigma_xz = function_wrappers.constant_fn(self.sigma_xz_uniform)
            self.sigma_yz = function_wrappers.constant_fn(self.sigma_yz_uniform)

    def generate_plots(self, **kwargs):
        if not self.figures:
            return

        # Collect data
        self.logger.debug('Generating geologic model manager plots')
        grid = kwargs.get('grid')
        wells = kwargs.get('wells')

        # Generate plots using the orion grid
        x_range, y_range = grid.get_plot_range()
        Nx = len(grid.x)
        Ny = len(grid.y)

        # Permeability
        k_range = [0.0, 1.0]
        k = np.zeros((Nx, Ny))
        if self.permeability:
            G = np.meshgrid(grid.x, grid.y)
            k = self.permeability(*G)
            k_range = [np.amin(k), np.amax(k)]

        if (k_range[1] == k_range[0]):
            k_range[1] += 1.0

        # Well overlay
        well_x, well_y, well_z = wells.get_plot_location(grid)

        # Setup figures
        ax = self.figures['permeability']['handle'].axes[0]
        old_visibility = plot_tools.getPlotVisibility(ax)
        ax.cla()
        cfig = self.figures['permeability']['extra_axis']
        cax = cfig.axes[0]
        cax.cla()

        ca = ax.imshow(np.flipud(k),
                       extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
                       aspect='auto',
                       interpolation='bilinear',
                       label='Permeability',
                       vmin=k_range[0],
                       vmax=k_range[1],
                       cmap=gui_colors.pressure_colormap,
                       visible=old_visibility['Permeability'])
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        plot_tools.setupColorbar(cfig, ca, cax, k_range, 'Permeability (mD)')

        ax.plot(well_x, well_y, label='Wells', visible=old_visibility['Wells'], **gui_colors.well_style)

    def load_table_files(self, fname):
        """
        Load structured or unstructured property values
        from an hdf5 format file

        Attributes:
            fname: Target file name
        """
        tmp = hdf5_wrapper.hdf5_wrapper(fname)
        data = tmp.get_copy()
        return table_files.load_table_files(data)
