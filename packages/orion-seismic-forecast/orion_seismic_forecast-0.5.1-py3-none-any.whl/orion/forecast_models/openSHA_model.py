# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
openSHA_model.py
-----------------------
"""

from orion.forecast_models import forecast_model_base
import numpy as np


class OpenSHAModel(forecast_model_base.ForecastModel):
    """
    OpenSHA forecast model

    Attributes:
        active (bool): Flag to indicate whether the model is active
        pressure_method (str): Pressure calculation method
        forecast_time (ndarray): Time values for forecast calculation
    """

    def set_class_options(self, **kwargs):
        """
        openSHA model initialization

        """
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.short_name = 'openSHA'
        self.long_name = 'openSHA'

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        # Example data access
        # Note: you can see what data lives in this class
        #       by looking at this class, and it's base class
        #       (forecast_model_base.ForecastModel)

        # # Seismic catalog holds raw data, shared seismic
        # # characteristics (a, b, etc.)
        # self.logger.debug('    Length of catalog = %i' % (seismic_catalog.N))
        # self.logger.debug('    Gutenberg-Richter: a = %1.2f, b = %1.2f' % (seismic_catalog.a_value, seismic_catalog.b_value))

        # # Calculate values directly from the base data
        # mean_x = np.mean(seismic_catalog.get_easting())
        # mean_y = np.mean(seismic_catalog.get_northing())
        # mean_z = np.mean(seismic_catalog.get_depth())
        # self.logger.debug('    location mean = (%1.2f, %1.2f, %1.2f) m' % (mean_x, mean_y, mean_z))
        # self.logger.debug('    UTM zone = %i%s' % (seismic_catalog.utm_zone[0], seismic_catalog.utm_zone[1]))

        # # Note: Time values within Orion are given as the unix epoch
        # #       (number of seconds since Jan 1, 1970)
        # #       Also, catalog entries should be sorted by time
        # t = seismic_catalog.get_epoch()
        # start_time_str = datetime.datetime.fromtimestamp(t).strftime('%m/%d/%Y')
        # t_range = t[-1] - t[0]
        # self.logger.debug('    Catalog start time: %s' % (start_time_str))
        # self.logger.debug('    Catalog time: %1.1f days' % (t_range / (60 * 60 * 24)))

        # # Fluid injection holds raw data, shared pumping characteristics
        # # Note: We will need to choose the shared parameters,
        # #       decide how to handle multiple wells, location data, etc.
        # # Flow rate currently has units of m3/min
        # max_q = np.amax(self.fluid_injection.flow_rate)
        # self.logger.debug('    Max flow rate = %1.2f (m3/min)' % (max_q))

        # # Pressure currently has units of kPa
        # max_p = np.amax(self.fluid_injection.pressure)
        # self.logger.debug('    Max pressure = %1.2f (kPa)' % (max_p))

        # For now, a forecast model is expected to set these two
        # values, which represent the forecasted magnitude rate in time
        # Note: It's ok if the time vector doesn't match the other
        #       forecast models, since they will be re-interpolated
        #       onto a common grid
        self.logger.debug('    (setting forecast to random array)')
        N = grid.shape
        self.temporal_forecast = np.cumsum(np.random.randint(0, 5, N[3]))
        self.spatial_forecast = np.random.randn(*N)

        return self.temporal_forecast, self.spatial_forecast
