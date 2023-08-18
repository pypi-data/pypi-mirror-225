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
import os
import sys
from pathlib import Path

package_path = os.path.abspath(Path(__file__).resolve().parents[1])
mod_path = os.path.abspath(os.path.join(package_path, 'src'))
sys.path.append(mod_path)
strive_path = os.path.abspath(os.path.join(package_path, '..', 'strive', 'src'))
sys.path.append(strive_path)


class TestWells():
    """
    Test various well manager, well data holder methods
    """

    def build_grid(self):
        """
        Build a grid required for some well analysis methods
        """
        from orion.managers import grid_manager
        test_grid = grid_manager.GridManager()
        test_grid.t = np.linspace(0.0, 10.0, 11)
        test_grid.t_origin = 0.0
        return test_grid

    def data(self, case):
        """
        Data for test cases. These include a set of wells with initial t, q values,
        and expected volume, rate changes over time.

        Args:
            case (str): Case name

        Returns:
            dict: test data
        """
        test_data = {}
        test_data['a'] = {
            't': [-1.0],
            'q': [0.1],
            'dv': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'dq': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        }
        test_data['b'] = {
            't': [-1.0, 0.0],
            'q': [0.1, -0.1],
            'dv': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'dq': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }
        test_data['c'] = {
            't': [-1.0, 0.0, 1.0],
            'q': [0.1, -0.1, -0.1],
            'dv': [0.00, -0.05, -0.15, -0.25, -0.35, -0.45, -0.55, -0.65, -0.75, -0.85, -0.95],
            'dq': [0.0, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1]
        }
        test_data['d'] = {
            't': [-1.0, 0.0, 1.0, 5.0],
            'q': [0.1, -0.1, -0.1, 0.2],
            'dv': [0.00, -0.05, -0.15, -0.25, -0.35, -0.35, -0.25, -0.15, -0.05, 0.05, 0.15],
            'dq': [0.0, -0.1, -0.1, -0.1, -0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        }
        return test_data[case]

    def assemble_wells(self, to_wells, q_wells):
        """
        Open an instance of the well manager and add wells to it

        Args:
            to_wells (list): List of pump start times
            q_wells (list): Pumping rates

        Returns:
            orion.managers.well_manager.WellManager: The well manager
        """
        from orion.managers import well_manager
        wells = well_manager.WellManager()
        for ii, (t, q) in enumerate(zip(to_wells, q_wells)):
            k = f'well_{ii:02d}'
            wells.add_child(k)
            wells.children[k].init_time = t
            wells.children[k].flow_rate = q
        return wells

    def test_add_well(self):
        """
        Test adding a well to the manager
        """
        wells = self.assemble_wells([0], [0])
        assert len(wells.children) == 1

    @pytest.mark.parametrize('case', ['a', 'b', 'c', 'd'])
    def test_well_parameters(self, case):
        """
        Test well parameter methods

        Args:
            case (str): Case name
            grid (orion.managers.grid_manager.GridManager): The problem grid
        """
        d = self.data(case)
        wells = self.assemble_wells(d['t'], d['q'])
        grid = self.build_grid()
        wells.calculate_well_parameters(grid)
        assert np.allclose(wells.net_volume, d['dv'])
        assert np.allclose(wells.net_dqdt, d['dq'])
