# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import pytest
import numpy as np
import tempfile
from scipy.special import exp1
import os
import sys
from pathlib import Path

package_path = os.path.abspath(Path(__file__).resolve().parents[1])
mod_path = os.path.abspath(os.path.join(package_path, 'src'))
sys.path.append(mod_path)
strive_path = os.path.abspath(os.path.join(package_path, '..', 'strive', 'src'))
sys.path.append(strive_path)


class TestSingleWellFlow():

    @pytest.fixture(scope='class')
    def paths(self):
        test_paths = {'root': tempfile.TemporaryDirectory()}
        test_paths['pressure_only'] = f"{test_paths['root'].name}/pressure_only.hdf5"
        test_paths['dpdt_only'] = f"{test_paths['root'].name}/dpdt_only.hdf5"
        test_paths['pressure_dpdt'] = f"{test_paths['root'].name}/pressure_dpdt.hdf5"
        return test_paths

    @pytest.fixture(scope='class')
    def grid(self):
        from orion.managers import grid_manager
        test_grid = grid_manager.GridManager()
        test_grid.x = np.linspace(1, 2, 2)
        test_grid.y = np.linspace(3, 4, 3)
        test_grid.z = np.linspace(5, 6, 4)
        test_grid.t = np.linspace(7, 8, 5)
        test_grid.t_origin = 0.0
        return test_grid

    @pytest.fixture(scope='class')
    def rfm(self):
        from orion.pressure_models import radial_flow

        # Choose parameters so that model scaling equals 1
        rfm = radial_flow.RadialFlowModel()
        rfm.wells_xyz = np.array([[0, 0, 0]])
        rfm.wells_to = np.array([0])
        rfm.wells_q = np.array([np.pi / (1000.0 * 9.81)])
        rfm.viscosity = 4.0 * 1000.0 * 9.81 * 1e-13
        rfm.permeability = 1.0
        rfm.storativity = 1.0
        rfm.payzone_thickness = 1.0
        return rfm

    @pytest.fixture(scope='class')
    def data(self, rfm, grid):
        # Evaluate the pressure model on a grid
        grid_values = np.meshgrid(grid.x, grid.y, grid.z, grid.t, indexing='ij')
        p = np.ascontiguousarray(rfm.p(*grid_values))
        dpdt = np.ascontiguousarray(rfm.dpdt(*grid_values))
        return p, dpdt

    def check_value_with_tolerance(self, value, expected):
        assert value == pytest.approx(expected, abs=1e-6)

    def test_pressure(self, rfm):
        p_a = rfm(1.0, 0.0, 0.0, 1.0)
        p_b = exp1(1.0)
        self.check_value_with_tolerance(p_a, p_b)

    def test_dpdt(self, rfm):
        dpdt_a = rfm.dpdt(1.0, 0.0, 0.0, 1.0)
        dpdt_b = np.exp(-1.0)
        self.check_value_with_tolerance(dpdt_a, dpdt_b)

    def test_dpdt_fd(self, rfm):
        N = 1000
        test_t = np.linspace(1.0, 10.0, N)
        test_t_mid = 0.5 * (test_t[1:] + test_t[:-1])
        p = [rfm(1.0, 0.0, 0.0, t) for t in test_t]
        dpdt = [rfm.dpdt(1.0, 0.0, 0.0, t) for t in test_t_mid]
        dpdt_fd = np.diff(p) / np.diff(test_t)
        assert np.allclose(dpdt, dpdt_fd)

    def test_write_gridded_files(self, rfm, grid, data, paths):
        from orion.utilities import hdf5_wrapper
        p, dpdt = data

        with hdf5_wrapper.hdf5_wrapper(paths['pressure_only'], mode='w') as tmp:
            tmp['x'] = grid.x
            tmp['y'] = grid.y
            tmp['z'] = grid.z
            tmp['t'] = grid.t
            tmp['pressure'] = p

        with hdf5_wrapper.hdf5_wrapper(paths['dpdt_only'], mode='w') as tmp:
            tmp['x'] = grid.x
            tmp['y'] = grid.y
            tmp['z'] = grid.z
            tmp['t'] = grid.t
            tmp['dpdt'] = dpdt

        with hdf5_wrapper.hdf5_wrapper(paths['pressure_dpdt'], mode='w') as tmp:
            tmp['x'] = grid.x
            tmp['y'] = grid.y
            tmp['z'] = grid.z
            tmp['t'] = grid.t
            tmp['pressure'] = p
            tmp['dpdt'] = dpdt

    @pytest.mark.parametrize('table_name, offset', [('pressure_only', False), ('dpdt_only', True),
                                                    ('pressure_dpdt', False)])
    def test_pressure_tables(self, table_name, offset, grid, data, paths):
        from orion.pressure_models import pressure_table

        # Load the pressure table
        pt = pressure_table.PressureTableModel()
        pt.file_name = paths[table_name]
        pt.run(grid, None, None)

        # Get the expected copy of the data
        p = data[0].copy()
        dpdt = data[1]
        if offset:
            p_init = p[:, :, :, 0].copy()
            for ii in range(len(grid.t)):
                p[:, :, :, ii] -= p_init

        # There can sometimes be derivative artefacts along the array edges,
        # so ignore these in the comparison
        assert np.allclose(p[..., 1:-1], pt.p_grid[..., 1:-1], atol=2e-5)
        assert np.allclose(dpdt[..., 1:-1], pt.dpdt_grid[..., 1:-1], atol=2e-5)
