# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
radial_flow.py
-----------------------
"""

import numpy as np
from orion.pressure_models import pressure_model_base
from orion.utilities import table_files
from scipy.special import exp1


class RadialFlowModel(pressure_model_base.PressureModelBase):
    """
    Pressure model based off of Theis Solution

    Attributes:
        viscosity (float): Fluid viscosity (cP)
        permeability (float): Matrix permeability (nD)
        storativity (float): Reservoir storativity factor
        payzone_thickness (float): Reservoir thickness
        min_radius (float): Minimum radius for solution
        wells_xyz (list): Well loctions (m)
        wells_to (list): Well start times (s)
        wells_q (list): Well flow rates (m3/s)
        min_dt_numerical (float): Minimum dt value used to avoid FPE's

    """

    def set_class_options(self, **kwargs):
        """
        Initialization function

        """
        # Model configuration
        self.short_name = 'Radial Flow'
        self.viscosity = 1.0
        self.permeability = 1.0
        self.storativity = 1.0e-3
        self.payzone_thickness = 1.0
        self.min_radius = 1.0
        self.t_origin = 0.0
        self.min_dt_numerical = 1.0
        self.export_grid_to_file = ''
        self.display_progress = False

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.wells_xyz = []
        self.wells_to = []
        self.wells_q = []

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Add values to gui
        self.gui_elements['viscosity'] = {
            'element_type': 'entry',
            'label': 'Viscosity',
            'position': [0, 0],
            'units': '(cP)'
        }
        self.gui_elements['permeability'] = {
            'element_type': 'entry',
            'label': 'Permeability',
            'position': [1, 0],
            'units': '(mD)'
        }
        self.gui_elements['storativity'] = {'element_type': 'entry', 'label': 'Storativity', 'position': [2, 0]}
        self.gui_elements['payzone_thickness'] = {
            'element_type': 'entry',
            'label': 'Unit thickness',
            'position': [3, 0],
            'units': '(m)'
        }
        self.gui_elements['min_dt_numerical'] = {
            'element_type': 'entry',
            'label': 'Well startup time',
            'position': [4, 0],
            'units': '(s)'
        }
        self.gui_elements['export_grid_to_file'] = {
            'element_type': 'entry',
            'label': 'Export results',
            'position': [5, 0],
            'units': '(*.hdf5, folder)'
        }

    def pressure_well(self, x, y, t, well_id, derivative=False):
        dt_actual = t + self.t_origin - self.wells_to[well_id]
        dt = np.maximum(dt_actual, self.min_dt_numerical)
        r = np.sqrt((x - self.wells_xyz[well_id, 0])**2 + (y - self.wells_xyz[well_id, 1])**2)

        unit_scale = 1e-13    # cP/mD
        K = unit_scale * self.permeability * 1000.0 * 9.81 / self.viscosity
        T = K * self.payzone_thickness
        b = r * r * self.storativity / (4.0 * T)
        u = b / dt
        u = np.minimum(np.maximum(u, 1e-6), 100.0)
        if derivative:
            # s = (-self.wells_q[well_id] / (4.0 * np.pi * T)) * (np.exp(-u) / u) * (-b / (dt * dt))
            s = (self.wells_q[well_id] / (4.0 * np.pi * T)) * np.exp(-u) / dt
        else:
            s = (self.wells_q[well_id] / (4.0 * np.pi * T)) * exp1(u)
        dp = s * 1000.0 * 9.81

        # Zero out negative time values
        if isinstance(dp, np.ndarray):
            dp[dt_actual < 0.0] = 0.0

        return dp

    def p(self, x, y, z, t):
        p = 1000.0 * 9.81 * z
        Nw = len(self.wells_to)
        for ii in range(Nw):
            p += self.pressure_well(x, y, t, ii)
            if self.display_progress:
                if ((ii % 100 == 0) or (ii == Nw - 1)):
                    progress = 100.0 * ii / (Nw)
                    self.logger.debug(f'p: {progress}%%')
        if self.display_progress:
            self.logger.debug('p: 100%%')
        return p

    def dpdt(self, x, y, z, t):
        p = 0.0 * z
        Nw = len(self.wells_to)
        for ii in range(Nw):
            p += self.pressure_well(x, y, t, ii, derivative=True)
            if self.display_progress:
                if ((ii % 100 == 0) or (ii == Nw - 1)):
                    progress = 100.0 * ii / (Nw)
                    self.logger.debug(f'p: {progress}%%')
        if self.display_progress:
            self.logger.debug('p: 100%%')
        return p

    def run(self, grid, well_manager, geologic_model):
        self.logger.debug('Setting up radial flow pressure model')

        # Save well data
        N = np.sum([well.N for well in well_manager.children.values()])
        self.wells_xyz = np.zeros((N, 3))
        self.wells_to = np.zeros(N)
        self.wells_q = np.zeros(N)

        ii = 0
        for well in well_manager.children.values():
            self.wells_xyz[ii, 0] = well.x
            self.wells_xyz[ii, 1] = well.y
            self.wells_xyz[ii, 2] = well.z
            self.wells_to[ii] = well.init_time
            self.wells_q[ii] = well.flow_rate
            ii += 1

            if len(well.variable_flow_rate):
                # Ignore zero-injection wells
                if (np.sum(abs(well.variable_flow_rate)) > 1e-10):
                    for jj in range(1, well.N):
                        self.wells_xyz[ii, 0] = well.x
                        self.wells_xyz[ii, 1] = well.y
                        self.wells_xyz[ii, 2] = well.z
                        self.wells_to[ii] = well.epoch[jj]
                        self.wells_q[ii] = well.variable_flow_rate[jj] - well.variable_flow_rate[jj - 1]
                        ii += 1

        # Evaluate on the grid
        self.grid_values(grid)

        if self.export_grid_to_file:
            self.logger.info(f'Exporting radial flow model results to: {self.export_grid_to_file}')
            data = {
                'x': grid.x,
                'y': grid.y,
                'z': grid.z,
                't': grid.t + grid.t_origin,
                'pressure': self.p_grid,
                'dpdt': self.dpdt_grid
            }
            table_files.save_table_files(self.export_grid_to_file, data)
