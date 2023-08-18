# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
forecast_model_base.py
-----------------------
"""

from orion.managers import manager_base
import numpy as np
import sys


class ForecastModel(manager_base.ManagerBase):
    """
    Base class for seismic forecast models

    Attributes:
        active (bool): Flag to indicate whether the model is active
        requires_catalog (bool): Flag to indicate whether the model needs a catalog
        temporal_forecast (np.ndarray): Cumulative number of forecasted number of events in time
        spatial_forecast (np.ndarray): Forecasted event count in voxels
    """

    def set_class_options(self, **kwargs):
        """
        Forecast model initialization
        """
        self.active = True
        self.requires_catalog = False

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.spatial_forecast = np.zeros(0)
        self.temporal_forecast = np.zeros(0)

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.gui_elements['long_name'] = {'element_type': 'text', 'position': [0, 0], 'columnspan': 2}
        self.gui_elements['active'] = {'element_type': 'check', 'label': 'Active', 'position': [1, 0]}

    def generate_forecast_permissive(self,
                                     grid,
                                     seismic_catalog,
                                     pressure,
                                     wells,
                                     geologic_model,
                                     catch_errors=False,
                                     remove_nan=True):
        res = []
        if catch_errors:
            try:
                res = self.generate_forecast(grid, seismic_catalog, pressure, wells, geologic_model)

            except AttributeError as error:
                self.logger.error('    model failed to run due to attribute error')
                self.logger.error('    message: ', error)
                self.logger.error(f'    {self.short_name}: {sys.exc_info()[-1].tb_lineno}')

            except IndexError as error:
                self.logger.error('    model failed to run due to indexing error')
                self.logger.error('    message: ', error)
                self.logger.error(f'    {self.short_name}: {sys.exc_info()[-1].tb_lineno}')

            except Exception as exception:
                self.logger.error('    model failed to run')
                self.logger.error('    message: ', exception)
                self.logger.error(f'    {self.short_name}: {sys.exc_info()[-1].tb_lineno}')
        else:
            res = self.generate_forecast(grid, seismic_catalog, pressure, wells, geologic_model)

        # Remove any nan values
        if remove_nan:
            for ii in range(len(res)):
                res[ii][np.isnan(res[ii])] = 0.0
        return res

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        """
        Model forecast run function

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
            pressure (orion.pressure_models.pressure_model_base.PressureModelBase): The current pressure model
            wells (orion.managers.well_manager.WellManager): The well data
            geologic_model (orion.managers.geologic_model_manager.GeologicModelManager): The current geological model

        Returns:
            tuple(np.ndarray, np.ndarray): temporal_forecast, spatial_forecast corresponding to grid
        """
        raise Exception("This should be overriden by the child class!")
