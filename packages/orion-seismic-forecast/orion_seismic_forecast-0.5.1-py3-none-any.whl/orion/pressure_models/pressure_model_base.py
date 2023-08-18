# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
pressure_model_base.py
-----------------------
"""

from orion.managers import manager_base
import numpy as np


class PressureModelBase(manager_base.ManagerBase):
    """
    Pressure model base class

    """

    def set_data(self, **kwargs):
        """
        Pressure model initialization

        """
        # Gridded values
        self.t_origin = 0.0
        self.p_grid = np.zeros(0)
        self.dpdt_grid = np.zeros(0)

    def __bool__(self):
        """
        Override for the default boolean operation
        """
        return True

    def __call__(self, *xargs):
        """
        If the object is called directly, pass the arguments to p
        """
        return self.p(*xargs)

    def p(self, x, y, z, t):
        """
        Evaluate the pressure model for a given location(s)

        Args:
            x (float, array): X location in the local coordinate system (m)
            y (float, array): Y location in the local coordinate system (m)
            z (float, array): Z location in the local coordinate system (m)
            t (float, array): Time in the local coordinate system (seconds)

        Returns:
            float: Pressure

        """
        return 0.0

    def dpdt(self, x, y, z, t):
        """
        Evaluate the pressure dpdt model for a given location(s)

        Args:
            x (float, array): X location in the local coordinate system (m)
            y (float, array): Y location in the local coordinate system (m)
            z (float, array): Z location in the local coordinate system (m)
            t (float, array): Time in the local coordinate system (seconds)

        Returns:
            float: First derivative of pressure with time

        """
        return 0.0

    def grid_values(self, grid):
        """
        Evaluates the pressure model on the current grid

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
        """
        G = np.meshgrid(grid.x, grid.y, grid.z, grid.t, indexing='ij')
        self.t_origin = grid.t_origin
        self.p_grid = self.p(*G)
        self.dpdt_grid = self.dpdt(*G)

    def run(self, grid, well_manager, geologic_model):
        """
        Runs the pressure model

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            well_manager (orion.managers.well_manager.WellManager): The Orion well manager
            geologic_model (orion.managers.geologic_model_manager.GeologicModelManager): The current geological model
        """
        pass
