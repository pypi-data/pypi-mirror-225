# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import itertools
import numpy as np
from orion.managers.manager_base import recursive
from orion.forecast_models import forecast_model_base

from ._helpers import rate


class RSODEModel(forecast_model_base.ForecastModel):

    def set_class_options(self, **kwargs):
        """
        Rate-and-state ODE model.

        Parameters
        ----------
        active : bool
            Flag to indicate whether the model is active.
        requires_catalog : bool
            Flag to indicate whether the model needs a catlog.
        pressure_method : str
            Pressure calculation method.
        forecast_time : :class:`numpy.ndarray`
            Time values for forecast calculation.
        forecast_cumulative_event_count : :class:`numpy.ndarray`
            Forecasted number of events.

        """
        # Call the parent's initialization
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.short_name = "RSODE"
        self.long_name = "Rate-and-State ODE Model"

        # Default values
        self.friction = 0.6
        self.background_rate_input = 1.0    # event/year
        self.stress_ini_input = 1.0e-5    # MPa/year
        self.asigma_input = 0.03    # MPa
        self.first_step_input = 1.0    # day
        self.max_step_input = 30.0    # day
        self.reduce_step_factor = 4.0
        self.reduce_step_max = 8
        self.rtol = 1.0e-5

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        super().set_data(**kwargs)
        self.background_rate = 1.0
        self.stress_ini = 1.0
        self.asigma = 1.0
        self.first_step = 1.0
        self.max_step = 1.0

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        super().set_gui_options(**kwargs)

        # GUI elements
        gui = {
            "friction": {
                "element_type": "entry",
                "label": "Coefficient of friction",
                "position": [4, 0],
            },
            "background_rate_input": {
                "element_type": "entry",
                "label": "Background seismicity rate",
                "position": [5, 0],
                "units": "(events/year)"
            },
            "stress_ini_input": {
                "element_type": "entry",
                "label": "Background stressing rate",
                "position": [6, 0],
                "units": "(MPa/year)",
            },
            "asigma_input": {
                "element_type": "entry",
                "label": u"A\u03C3 parameter",
                "position": [7, 0],
                "units": "(MPa)",
            },
            "first_step_input": {
                "element_type": "entry",
                "label": "Initial time step size",
                "position": [4, 1],
                "units": "(day)",
            },
            "max_step_input": {
                "element_type": "entry",
                "label": "Maximum time step size",
                "position": [5, 1],
                "units": "(day)",
            },
            "reduce_step_factor": {
                "element_type": "entry",
                "label": "Time step reduction factor",
                "position": [6, 1],
            },
            "reduce_step_max": {
                "element_type": "entry",
                "label": "Maximum number of time step reduction",
                "position": [7, 1],
            },
            "rtol": {
                "element_type": "entry",
                "label": "Relative convergence tolerance",
                "position": [8, 1],
            },
        }
        self.gui_elements.update(gui)

    @recursive
    def process_inputs(self):
        """Convert input units to SI units."""
        self.background_rate = self.background_rate_input / (365.25 * 86400.0)    # event/second
        self.stress_ini = self.stress_ini_input * 1.0e6 / (365.25 * 86400.0)    # Pa/second
        self.asigma = self.asigma_input * 1.0e6    # Pa
        self.first_step = self.first_step_input * 86400.0    # second
        self.max_step = self.max_step_input * 86400.0    # second

    def generate_forecast(
        self,
        grid,
        seismic_catalog,
        pressure,
        wells,
        geologic_model,
    ):
        """
        Model forecast run function.

        Parameters
        ----------
        grid : :class:`orion.managers.grid_manager.GridManager`
            The Orion grid manager.
        seismic_catalog : :class:`orion.managers.seismic_catalog.SeismicCatalog`
            The current seismic catalog.
        pressure : :class:`orion.pressure_models.pressure_model_base.PressureModelBase`
            The current pressure model.
        wells : :class:`orion.managers.well_manager.WellManager`
            The well data.
        geologic_model : :class:`orion.managers.geologic_model_manager.GeologicModelManager`
            The current geological model.

        """
        # Array dimensions
        nx = len(grid.x)
        ny = len(grid.y)
        nt = len(grid.t)

        # Times
        t = grid.t[:]
        tmax = t[-1]

        # Solver parameters
        dt = self.first_step
        dtmax = self.max_step
        dtfac = self.reduce_step_factor
        dt_reduce_max = self.reduce_step_max
        rtol = self.rtol

        # Use inverse to avoid repeated zero division check
        tci = self.stress_ini / self.asigma
        s0i = 1.0 / self.stress_ini

        # Time delta for integral
        dt_int = np.diff(t)
        dt_int = np.insert(dt_int, 0, dt_int[0])

        success = True
        self.forecast_time = grid.t.copy()
        self.spatial_forecast = np.zeros((nt, nx, ny))
        for i, j in itertools.product(range(nx), range(ny)):
            # Stressing rate
            s = self.friction * pressure.dpdt_grid[i, j, 0, :]
            s += self.stress_ini

            # Solve ODE
            r = rate(t, s, s0i, tci, tmax, dt, dtmax, dtfac, dt_reduce_max, rtol)

            # Check convergence
            if r[0] >= 0.0:
                self.spatial_forecast[:, i, j] = r * self.background_rate * dt_int

            else:
                success = False
                self.spatial_forecast[:] = 0.0
                break

        if success:
            self.spatial_forecast = np.cumsum(self.spatial_forecast, axis=0)
            self.temporal_forecast = np.sum(self.spatial_forecast, axis=(1, 2))

        else:
            self.logger.error(f"Convergence failure in Runge-Kutta solver for {self.short_name} model")
            self.temporal_forecast = np.zeros_like(grid.t)

        return self.temporal_forecast, self.spatial_forecast
