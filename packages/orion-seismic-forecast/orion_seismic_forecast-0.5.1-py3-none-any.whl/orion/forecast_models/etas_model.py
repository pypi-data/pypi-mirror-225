# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
etas_model.py
-----------------------
"""

from orion.forecast_models import forecast_model_base
import numpy as np


class ETASModel(forecast_model_base.ForecastModel):
    """
    ETAS forecast model

    """

    def set_class_options(self, **kwargs):
        """
        ETAS Model initialization

        """
        # Call the parent's initialization
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.short_name = 'ETAS'
        self.long_name = 'ETAS'

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        self.logger.warning('    (setting forecast to random array)')
        N = grid.shape
        self.temporal_forecast = np.cumsum(np.random.randint(0, 5, N[3]))
        self.spatial_forecast = np.random.randn(*N)

        return self.temporal_forecast, self.spatial_forecast
