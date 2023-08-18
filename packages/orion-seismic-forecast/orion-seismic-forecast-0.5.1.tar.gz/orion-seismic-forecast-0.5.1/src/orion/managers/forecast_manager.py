# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
forecast_manager.py
-----------------------
"""

from orion.managers import manager_base
from orion.forecast_models import list_ as forecast_models_list
from orion.utilities import plot_tools, statistical_methods, other
from orion.utilities.plot_config import gui_colors
from orion import _frontend
from functools import partial
import multiprocessing
import numpy as np
from sklearn import linear_model
from orion.managers.manager_base import recursive


class ForecastManager(manager_base.ManagerBase):
    """
    A class for managing the various seismic
    forecasting methods generated via ORION

    Attributes:
        forecast_data_start (str): The start time (mm/dd/yyyy) for the analysis (empty = beginning of catalog)
        forecast_data_stop (str): The end time (mm/dd/yyyy) for the analysis (empty = end of catalog)
        percent_ensemble_train (int): The percentage of the catalog to reserve for training the ensemble forecast
        percent_ensemble_test (int): The percentage of the catalog to reserve for testing the ensemble forecast
        train_split_epoch (float): Timestamp at the end of the training segment
        forecast_split_epoch (float): Timestamp at the end of the testing segment
        forecast_end_epoch (float): Timestamp at the end of the forecast
        forecast_length (float): The length of the requested forecast (years)
        time_range (list): The current time slice under considration
        forecast_time (list): A list of time vectors produced by the forcast models
        forecast_cumulative_event_count (list): A list of forecast result vectors produced by the forcast models
    """

    def set_class_options(self, **kwargs):
        """
        Forecast manager initialization

        Setup empty data holders, configuration options,
        data sources, and gui configuration
        """

        # Set the shorthand name
        self.short_name = 'Forecast Models'

        # Add the available forecast models
        self.child_classes += forecast_models_list

        # Forecast options
        self.forecast_options_list = ['Use Grid', 'ML Training Style']
        self.current_forecast_option = self.forecast_options_list[0]

        # Ensemble calculation
        self.percent_model_train = 33
        self.percent_ensemble_train = 33
        self.percent_ensemble_test = 33
        self.train_split_epoch = 0.0
        self.forecast_split_epoch = 0.0
        self.forecast_end_epoch = 0.0

        # Exceedance plots
        self.exceedance_header = '\nMagnitude Exceedance Plots'
        self.exceedance_plot_time_input = 30.0
        self.exceedance_plot_time = 30.0
        self.exceedance_dial_plot_magnitude = 3.0
        self.exceedance_bar_plot_min_magnitude = 0.0
        self.exceedance_bar_plot_max_magnitude = 3.0
        self.exceedance_bar_plot_magnitude_number = 4
        self.exceedance_color_yellow_threshold = 30.0
        self.exceedance_color_red_threshold = 60.0

    def set_user_options(self, **kwargs):
        # Processing
        self.catch_forecast_errors = 1
        self.use_multiprocessing = 0

        # Plots
        self.useCumulativePlots = 1
        self.use_spatial_cumulative_plots = 0
        self.available_plot_methods = ['Average', 'Range', 'All']
        self.plot_method = self.available_plot_methods[0]

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        # Forecast objects
        self.current_forecasts = {}
        self.time_range = []
        self.forecast_time = np.zeros(0)
        self.forecast_cumulative_event_count = np.zeros(0)
        self.spatial_forecast_count = np.zeros((0, 0, 0))
        self.spatial_forecast_density_count = np.zeros((0, 0, 0))
        self.spatial_forecast_density_rate = np.zeros((0, 0, 0))
        self.spatial_forecast_exceedance = np.zeros((0, 0))
        self.exceedance_dial_plot_probability = 0.0
        self.exceedance_bar_plot_magnitudes = np.zeros(0)
        self.exceedance_bar_plot_probabilities = np.zeros(0)

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Add figure handles
        self.set_visibility_all()

        fig_size_a = (5, 3)
        fig_size_b = (8, 3)
        if _frontend == 'strive':
            fig_size_a = (45, 25)
            fig_size_b = (90, 40)

        self.figures = {
            'exceedance_month': {
                'position': [0, 0],
                'size': fig_size_a,
                'static': True,
                'target': 'exceedance_bar'
            },
            'dial_plot': {
                'position': [0, 1],
                'size': fig_size_a,
                'static': True,
                'target': 'exceedance_dial'
            },
            'event_count': {
                'position': [1, 0],
                'size': fig_size_b,
                'columnspan': 4,
                'layer_config': True,
                'target': 'forecast_lines'
            }
        }

        # Add Gui elements
        # Note: the keys point to the class members by name
        self.gui_elements['useCumulativePlots'] = {
            'element_type': 'check',
            'label': 'Cumulative plot (temporal)',
            'position': [0, 0]
        }
        self.gui_elements['use_spatial_cumulative_plots'] = {
            'element_type': 'check',
            'label': 'Cumulative plot (spatial)',
            'position': [1, 0]
        }

        self.gui_elements['plot_method'] = {
            'element_type': 'dropdown',
            'label': 'Plot type',
            'position': [2, 0],
            'values': self.available_plot_methods
        }

        # Disable these user inputs for now
        # self.gui_elements['current_forecast_option'] = {
        #     'element_type': 'dropdown',
        #     'label': 'Forecast Option',
        #     'position': [2, 0],
        #     'values': self.forecast_options_list
        # }

        # self.gui_elements['percent_ensemble_train'] = {
        #     'element_type': 'entry',
        #     'label': 'ML-style train, test',
        #     'position': [3, 0]
        # }

        # self.gui_elements['percent_ensemble_test'] = {
        #     'element_type': 'entry',
        #     'position': [3, 1],
        #     'units': '(%)',
        #     'units_span': 4
        # }

        self.gui_elements['exceedance_header'] = {'element_type': 'text', 'position': [4, 0]}

        self.gui_elements['exceedance_plot_time_input'] = {
            'element_type': 'entry',
            'label': 'Time range',
            'units': '(days)',
            'position': [5, 0],
            'units_span': 4
        }

        self.gui_elements['exceedance_dial_plot_magnitude'] = {
            'element_type': 'entry',
            'label': 'Dial magnitude',
            'position': [6, 0]
        }

        self.gui_elements['exceedance_bar_plot_min_magnitude'] = {
            'element_type': 'entry',
            'label': 'Bar plot bins',
            'position': [7, 0]
        }

        self.gui_elements['exceedance_bar_plot_max_magnitude'] = {'element_type': 'entry', 'position': [7, 1]}

        self.gui_elements['exceedance_bar_plot_magnitude_number'] = {
            'element_type': 'entry',
            'units': '(min, max, N)',
            'position': [7, 2]
        }

        self.gui_elements['exceedance_color_yellow_threshold'] = {
            'element_type': 'entry',
            'label': 'Color thresholds',
            'position': [8, 0]
        }

        self.gui_elements['exceedance_color_red_threshold'] = {
            'element_type': 'entry',
            'units': '(yellow, red, %)',
            'position': [8, 1],
            'units_span': 4
        }

        self.gui_elements['catch_forecast_errors'] = {
            'element_type': 'check',
            'label': 'Permissive',
            'position': [9, 0],
            'user': True
        }

        self.gui_elements['use_multiprocessing'] = {
            'element_type': 'check',
            'label': 'Parallel calculation',
            'position': [10, 0],
            'user': True
        }

    @recursive
    def process_inputs(self):
        # Setup bins
        self.exceedance_bar_plot_magnitudes = np.linspace(self.exceedance_bar_plot_max_magnitude,
                                                          self.exceedance_bar_plot_min_magnitude,
                                                          self.exceedance_bar_plot_magnitude_number)
        self.exceedance_bar_plot_probabilities = np.zeros(self.exceedance_bar_plot_magnitude_number)
        self.exceedance_dial_plot_probability = 0.0
        self.exceedance_plot_time = self.exceedance_plot_time_input * 60 * 60 * 24.0

    def run(self, grid, seismic_catalog, pressure_manager, wells, geologic_model):
        """
        Chooses the forecast manager style.

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
            pressure_manager (orion.managers.pressure_manager.PressureManager): The pressure manager
            wells (orion.managers.well_manager.WellManager): The well data
            geologic_model (orion.managers.geologic_model_manager.GeologicModelManager): The current geological model
        """
        if (self.current_forecast_option == 'Use Grid'):
            self.run_grid_style(grid, seismic_catalog, pressure_manager, wells, geologic_model)
        elif (self.current_forecast_option == 'ML Training Style'):
            self.run_ml_style(grid, seismic_catalog, pressure_manager, wells, geologic_model)
        else:
            self.logger.error(f'Unrecognized forecast manager method: {self.current_forecast_option}')

        if seismic_catalog:
            self.estimate_magnitude_exceedance_probability(grid, seismic_catalog)

    def run_grid_style(self, grid, seismic_catalog, pressure_manager, wells, geologic_model):
        """
        Runs the forecast manager on the grid, expects results to be gridded

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
            pressure_manager (orion.managers.pressure_manager.PressureManager): The pressure manager
            wells (orion.managers.well_manager.WellManager): The well data
            geologic_model (orion.managers.geologic_model_manager.GeologicModelManager): The current geological model
        """
        self.logger.info('Runing manager in grid-style...')
        seismic_catalog.reset_slice()
        self.generate_model_forecasts(grid, seismic_catalog, pressure_manager, wells, geologic_model)

        # Generate the ensemble forecast
        self.logger.info('Calculating ensemble forecast...')
        self.estimate_weights_linear_regression(seismic_catalog)
        self.calculate_weighted_cumulative_forecast(grid)

    def estimate_magnitude_exceedance_probability(self, grid, seismic_catalog):
        """
        Estimates the probability events will exceed a given user-defined magnitude (self.exceedance_dial_plot_magnitude,
        self.exceedance_bar_plot_magnitudes) during the next time period (self.exceedance_plot_time_input).
        The calculation is performed for the entire area, and for individual grid cells.

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
        """
        # Note: Should we be considering all of catalog here,
        #       or a user-defined past period?  This can certainly effect the b-value

        # Global values
        # seismic_catalog.set_slice(-1e99, 0.0)
        # seismic_catalog.reset_slice()
        if not len(self.forecast_cumulative_event_count):
            return

        # Set the active slice
        ts = (grid.snapshot_time * 60 * 60 * 24.0)
        seismic_catalog.set_slice(time_range=[-1e99, ts])
        Ia = np.argmin(abs(ts - self.forecast_time))

        # Target sizes
        Nx = len(grid.x)
        Ny = len(grid.y)
        M = np.shape(self.spatial_forecast_count)
        self.spatial_forecast_exceedance = np.zeros((Nx, Ny))

        # Estimate exceedance
        self.exceedance_bar_plot_probabilities = statistical_methods.poisson_probability(
            self.forecast_time, self.forecast_cumulative_event_count, seismic_catalog.b_value,
            seismic_catalog.magnitude_completeness, self.exceedance_bar_plot_magnitudes, self.exceedance_plot_time)

        if np.isnan(seismic_catalog.magnitude_completeness):
            self.logger.debug("There are not enough active events to estimate exceedance")
            return

        tmp = statistical_methods.poisson_probability(self.forecast_time, self.forecast_cumulative_event_count,
                                                      seismic_catalog.b_value, seismic_catalog.magnitude_completeness,
                                                      np.array([self.exceedance_dial_plot_magnitude]),
                                                      self.exceedance_plot_time)
        self.exceedance_dial_plot_probability = tmp[0]

        # Grid based values
        if (Ia == 0):
            return

        t = self.forecast_time[:Ia]
        if ((M[1] == Nx) & (M[2] == Ny)):
            spatial_exceedance_magnitude = np.array([self.exceedance_dial_plot_magnitude])
            for ii in range(Nx):
                for jj in range(Ny):
                    c = self.spatial_forecast_count[:Ia, ii, jj]
                    tmp = statistical_methods.poisson_probability(t, c, seismic_catalog.b_value,
                                                                  seismic_catalog.magnitude_completeness,
                                                                  spatial_exceedance_magnitude,
                                                                  self.exceedance_plot_time)
                    self.spatial_forecast_exceedance[ii, jj] = tmp[0]

    def calculate_weighted_cumulative_forecast(self, grid):
        """
        Calculate the weighted cumulative spatial and temporal forecasts

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
        """

        Nx, Ny, Nz, Nt = grid.shape
        self.forecast_cumulative_event_count = np.zeros(Nt)
        self.spatial_forecast_count = np.zeros((Nt, Nx, Ny))

        # for fa in self.current_forecasts.values():
        for k, fa in self.current_forecasts.items():
            for fb in fa.values():
                for fc in fb.values():
                    self.forecast_cumulative_event_count += fc['temporal'] * fc['weight']
                    self.spatial_forecast_count += fc['spatial'] * fc['weight']

        # Calculate event/density estimates (N/m^2, N/s*m^2)
        self.spatial_forecast_density_count = self.spatial_forecast_count / np.expand_dims(grid.areas, 0)
        self.spatial_forecast_density_rate = other.derivative(self.spatial_forecast_density_count, grid.t, axis=0)

    def generate_model_forecasts(self, grid, seismic_catalog, pressure_manager, wells, geologic_model):
        """
        Generate forecasts for the current time slice

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
            pressure_manager (orion.managers.pressure_manager.PressureManager): The pressure manager
            wells (orion.managers.well_manager.WellManager): The well data
            geologic_model (orion.managers.geologic_model_manager.GeologicModelManager): The current geological model
            forecast_length (float): The length of the requested forecast (seconds)
        """
        self.current_forecasts = {}
        self.forecast_time = grid.t.copy()

        # Assemble a list of active children
        active_children = [k for k in self.children.keys() if self.children[k].active]
        if self.use_multiprocessing:
            # Execute forecasts in subprocesses
            pfunc = partial(run_parallel_forecast, self, grid, seismic_catalog, pressure_manager, wells, geologic_model)
            pool = multiprocessing.Pool(processes=len(active_children))
            parallel_results = pool.map(pfunc, active_children)
            pool.close()
            pool.join()
            for ii, k in enumerate(active_children):
                self.current_forecasts[k] = parallel_results[ii]
        else:
            # Exectute forecasts in serial
            for ka, f in self.children.items():
                if f.active:
                    self.current_forecasts[ka] = {}
                    for kb, pressure in pressure_manager.active_pressure_models.items():
                        self.current_forecasts[ka][kb] = {}
                        for kc, catalog in seismic_catalog.decluster_realizations():
                            tmp = self.children[ka].generate_forecast_permissive(
                                grid,
                                seismic_catalog,
                                pressure,
                                wells,
                                geologic_model,
                                catch_errors=self.catch_forecast_errors)
                            if tmp:
                                self.current_forecasts[ka][kb][kc] = {
                                    'temporal': tmp[0],
                                    'spatial': tmp[1],
                                    'weight': 1.0
                                }
                            else:
                                self.logger.error(
                                    f'Forecast calculation failed: model={ka}, pressure realization={kb}, decluster realization={kc}'
                                )

    def parse_timing_requests(self):
        """
        Parse the timing requests for forecast training
        """
        # Set the time range
        if self.forecast_data_start:
            self.time_range[0] = float(self.forecast_data_start) * 60.0 * 60.0 * 24.0

        if self.forecast_data_stop:
            self.time_range[1] = float(self.forecast_data_stop) * 60.0 * 60.0 * 24.0

        # Setup model splitting
        self.percent_ensemble_train = int(self.percent_ensemble_train)
        self.percent_ensemble_test = int(self.percent_ensemble_test)

        # Check to make sure values are reasonable
        if (self.percent_ensemble_train < 0):
            self.percent_ensemble_train = 0
            self.logger.warning('Warning: percent_ensemble_train must be >= 0, setting value to 0...')

        if (self.percent_ensemble_test < 0):
            self.percent_ensemble_test = 0
            self.logger.warning('Warning: percent_ensemble_test must be >= 0, setting value to 0...')

        ensemble_percent = self.percent_ensemble_train + self.percent_ensemble_test
        if (ensemble_percent > 100):
            self.percent_ensemble_train = int(self.percent_ensemble_train * 0.01 / ensemble_percent)
            self.percent_ensemble_test = int(self.percent_ensemble_test * 0.01 / ensemble_percent)
            self.logger.warning(
                'Warning: percent_ensemble_train + percent_ensemble_test must be <= 100, rescaling values...')

        self.percent_model_train = 100 - self.percent_ensemble_train - self.percent_ensemble_test
        catalog_length = self.time_range[1] - self.time_range[0]
        self.train_split_epoch = self.time_range[0] + catalog_length * 0.01 * self.percent_model_train
        dc = catalog_length * 0.01 * (self.percent_model_train + self.percent_ensemble_train)
        self.forecast_split_epoch = self.time_range[0] + dc
        self.forecast_end_epoch = self.time_range[1] + self.forecast_length * 60.0 * 60.0 * 24.0 * 365.25

    def estimate_weights_linear_regression(self, seismic_catalog):
        """
        Estimate decision tree linear weights

        Args:
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
        """
        # Flatten the forecast results
        flat_keys = []
        flat_forecasts = []
        for ka, fa in self.current_forecasts.items():
            for kb, fb in fa.items():
                for kc, fc in fb.items():
                    flat_keys.append([ka, kb, kc])
                    flat_forecasts.append(fc['temporal'])

        # Calculate the magnitude rate for the equivalent catalog data
        # Note: use the full (non-declustered) catalog
        # seismic_catalog.finalize_slice()
        seismic_catalog.reset_slice()
        catalog_ne_t, catalog_ne = seismic_catalog.calculate_cumulative_event_count(self.forecast_time)

        # Use sklearn to perform a multiple linear regression
        clf = linear_model.LinearRegression(positive=True)
        if len(catalog_ne):
            clf.fit(np.transpose(np.array(flat_forecasts)), catalog_ne)
            for ii, k in enumerate(flat_keys):
                self.current_forecasts[k[0]][k[1]][k[2]]['weight'] = clf.coef_[ii]

    def run_ml_style(self, grid, seismic_catalog, pressure_manager, wells, geologic_model):
        """
        Runs the forecast manager and generates an ensemble forecast

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
            seismic_catalog (orion.managers.seismic_catalog.SeismicCatalog): The current seismic catalog
            pressure_manager (orion.managers.pressure_manager.PressureManager): The pressure manager
            wells (orion.managers.well_manager.WellManager): The well data
            geologic_model (orion.managers.geologic_model_manager.GeologicModelManager): The current geological model
        """
        # Note: these need to be updated to work:
        self.logger.warning('ML style forecasts not enabled')
        return

        # Setup timing
        self.time_range = [-1.0, 0.0]
        if seismic_catalog:
            self.time_range[0] = np.amin(seismic_catalog.epoch) - grid.t_origin
        self.parse_timing_requests()

        # Set the catalog slices for individual model training
        train_slice = [self.time_range[0], self.train_split_epoch]
        seismic_catalog.set_slice(time_range=train_slice, seismic_characteristics_dt=grid.dt * 60 * 60 * 24)

        # Generate the model forecasts for the training data
        self.logger.info('Training ensemble forecast...')
        self.generate_model_forecasts(grid, seismic_catalog, pressure_manager, wells, geologic_model)

        # Determine the weights using a simple linear regression
        # Set the catalog slices for individual ensemble training, forecasting
        train_slice[1] = self.forecast_split_epoch
        seismic_catalog.set_slice(time_range=train_slice)
        self.estimate_weights_linear_regression(seismic_catalog)

        # Generate the ensemble forecast
        self.logger.info('Calculating ensemble forecast...')
        seismic_catalog.reset_slice()
        self.generate_model_forecasts(grid, seismic_catalog, pressure_manager, geologic_model)
        self.calculate_weighted_cumulative_forecast(grid)

        # Reset the global time slice
        self.logger.info('Done!')

    def check_plot_style(self, t, x):
        """
        Handle user requests for cumulative/rate plots

        Args:
            t (np.ndarray): Times
            x (np.ndarray): Cumulative values

        Returns:
            np.ndarray: Cumulative or rate-based values
        """
        if not len(x):
            return x
        elif self.useCumulativePlots:
            return x
        else:
            ts = 60.0 * 60.0 * 24.0
            return other.derivative(x, t) * ts

    def get_plot_data(self, projection):
        rate_scale = 1e6 * 60.0 * 60.0 * 24.0 * 365.25
        rate_units = '#/year*km^2'
        target_rate_field = self.spatial_forecast_density_rate * rate_scale
        return {
            'spatial_forecast_rate': target_rate_field,
            'spatial_forecast_rate_units': rate_units,
            'spatial_forecast_count': self.spatial_forecast_density_count,
            'spatial_forecast_count_units': '#/km^2'
        }

    def exceedance_bar(self, plot_data):
        exceedance_title = f'Exceedance probability within {self.exceedance_plot_time_input:1.1f} days'
        c = []
        for p in self.exceedance_bar_plot_probabilities:
            if p < self.exceedance_color_yellow_threshold:
                c.append('green')
            elif p < self.exceedance_color_red_threshold:
                c.append('yellow')
            else:
                c.append('red')

        layers = {
            'exceedance': {
                'y': self.exceedance_bar_plot_magnitudes,
                'x': self.exceedance_bar_plot_probabilities,
                'c': c,
                'type': 'bar',
                'orientation': 'h'
            }
        }
        axes = {'x': exceedance_title, 'y': 'Magnitude'}
        return layers, axes

    def exceedance_dial(self, plot_data):
        dial_label = f'p(magnitude > {self.exceedance_dial_plot_magnitude:1.1f}) within {self.exceedance_plot_time_input:1.1f} days'

        steps = [{
            'range': [0, self.exceedance_color_yellow_threshold],
            'color': 'green'
        }, {
            'range': [self.exceedance_color_yellow_threshold, self.exceedance_color_red_threshold],
            'color': 'yellow'
        }, {
            'range': [self.exceedance_color_red_threshold, 100.0],
            'color': 'red'
        }]

        layers = {
            'exceedance': {
                'x': self.exceedance_dial_plot_probability,
                'c': 'gray',
                'type': 'dial',
                'steps': steps
            }
        }
        axes = {'x': dial_label, 'x_range': [0, 100]}
        return layers, axes

    def forecast_lines(self, plot_data):
        seismic_plot_data = plot_data['Seismic Catalog']
        time_scale = 1.0 / (60.0 * 60.0 * 24.0)
        t = self.forecast_time * time_scale

        catalog_ne = seismic_plot_data.get('catalog_cumulative_event_count', np.zeros(0))
        catalog_ne_t = seismic_plot_data.get('catalog_cumulative_event_count_t', np.zeros(0))
        catalog_ne_t *= time_scale

        layers = {
            'Catalog': {
                'x': catalog_ne_t,
                'y': catalog_ne,
                'type': 'line'
            },
            'Ensemble': {
                'x': t,
                'y': self.forecast_cumulative_event_count,
                'type': 'line'
            }
        }

        for ka, forecast_model in self.children.items():
            main_label = forecast_model.short_name
            if ka in self.current_forecasts:
                for kb, fb in self.current_forecasts[ka].items():
                    for kc, fc in fb.items():
                        layers[main_label] = {'x': t, 'y': fc['temporal'], 'type': 'line'}

        axes = {'x': 'Time (days)', 'y': 'Event Count'}
        return layers, axes

    def update_plot_data(self, **kwargs):
        grid = kwargs['GridManager']
        seismic_catalog = kwargs['SeismicCatalog']
        if seismic_catalog:
            self.estimate_magnitude_exceedance_probability(grid, seismic_catalog)

    def generate_plots(self, **kwargs):
        # Collect data
        self.logger.debug('Generating forecast manager plots')
        grid = kwargs.get('grid')
        seismic_catalog = kwargs.get('seismic_catalog')

        # Setup timing
        time_scale = 1.0 / (60.0 * 60.0 * 24.0)

        # Plot colors
        color_thresholds = [self.exceedance_color_yellow_threshold, self.exceedance_color_red_threshold]

        # Bar plot
        ax = self.figures['exceedance_month']['handle'].axes[0]
        ax.cla()
        plot_tools.exceedance_bar_plot(ax,
                                       self.exceedance_bar_plot_magnitudes,
                                       self.exceedance_bar_plot_probabilities,
                                       color_lims=color_thresholds)
        ax.set_title(
            f'Probability of a seismic event exceeding\n target magnitude within {self.exceedance_plot_time_input:1.1f} days'
        )

        # Dial plot
        ax = self.figures['dial_plot']['handle'].axes[0]
        ax.cla()
        plot_tools.exceedance_dial_plot(ax, self.exceedance_dial_plot_probability, color_lims=color_thresholds)
        ax.set_title(
            f'p(magnitude > {self.exceedance_dial_plot_magnitude:1.1f}) within {self.exceedance_plot_time_input:1.1f} days'
        )

        # Event count plot
        ax = self.figures['event_count']['handle'].axes[0]
        ax.cla()
        max_number_events = 1
        catalog_ne_t = [0]

        if seismic_catalog:
            # Check the time range
            if not len(self.time_range):
                self.time_range = [-1.0, 0.0]
                if seismic_catalog:
                    self.time_range[0] = np.amin(seismic_catalog.epoch) - grid.t_origin

            # Get the catalog event rate
            catalog_ne_t, catalog_ne = seismic_catalog.calculate_cumulative_event_count(grid.t)
            catalog_ne = self.check_plot_style(catalog_ne_t, catalog_ne)

            # Plot the saved catalog event rate
            max_number_events = np.amax(catalog_ne)
            line_style = gui_colors.periodic_line_style(0)
            line_style['linewidth'] = 2
            ax.plot(catalog_ne_t * time_scale, catalog_ne, label='Catalog', **line_style)
        else:
            # Add an empty plot for figure control
            ax.plot([], [], 'k', linewidth=4, label='Catalog')

        # Joint forecast
        tf = self.forecast_time * time_scale
        nf = self.check_plot_style(self.forecast_time, self.forecast_cumulative_event_count)
        if len(nf):
            max_number_events = max(max_number_events, np.amax(nf))
        line_style = gui_colors.periodic_line_style(1)
        line_style['linewidth'] = 2
        ax.plot(tf, nf, label='Ensemble', **line_style)

        # Child forecasts
        plot_id = 2
        for ka, forecast_model in self.children.items():
            main_label = forecast_model.short_name
            if ka in self.current_forecasts:
                realizations = []
                for kb, fb in self.current_forecasts[ka].items():
                    for kc, fc in fb.items():
                        nf = self.check_plot_style(self.forecast_time, fc['temporal'])
                        max_number_events = max(max_number_events, np.amax(nf))
                        if (self.plot_method == 'All'):
                            realization_label = f'{main_label}_{kb}_{kc}'
                            line_style = gui_colors.periodic_line_style(plot_id)
                            plot_id += 1
                            ax.plot(tf, nf, label=realization_label, **line_style)
                        else:
                            realizations.append(nf)

                if (self.plot_method == 'Average'):
                    nf = np.nanmean(realizations, axis=0)
                    line_style = gui_colors.periodic_line_style(plot_id)
                    plot_id += 1
                    ax.plot(tf, nf, label=main_label, **line_style)

                elif (self.plot_method == 'Range'):
                    nf_min = np.nanmin(realizations, axis=0)
                    nf_max = np.nanmax(realizations, axis=0)
                    c = gui_colors.periodic_color_style(plot_id)['color']
                    plot_id += 1
                    ax.fill_between(tf, nf_min, nf_max, label=main_label, color=c)

            else:
                line_style = gui_colors.periodic_line_style(plot_id)
                plot_id += 1
                ax.plot([], [], label=main_label, **line_style)

        # Training/testing indicators
        if (self.current_forecast_option == 'ML Training Style'):
            ta = self.train_split_epoch * time_scale
            tb = self.forecast_split_epoch * time_scale
            tc = catalog_ne_t[-1] * time_scale
            ax.plot([ta, ta], [0, max_number_events], 'k--')
            ax.plot([tb, tb], [0, max_number_events], 'k--')
            ax.plot([tc, tc], [0, max_number_events], 'k--')

            if (tb > ta):
                ax.text(0.5 * (ta + tb),
                        0.9 * max_number_events,
                        '(ensemble training)',
                        horizontalalignment='center',
                        verticalalignment='center')
            if (tc > tb):
                ax.text(0.5 * (tb + tc),
                        0.9 * max_number_events,
                        '(ensemble testing)',
                        horizontalalignment='center',
                        verticalalignment='center')

        # Finalize the figure axes
        ax.legend(loc=2, ncol=2)
        if (max_number_events > 0):
            ax.set_ylim([0, max_number_events])
        if (grid.plot_time_min < grid.plot_time_max):
            ax.set_xlim([grid.plot_time_min, grid.plot_time_max])
        else:
            ax.set_xlim([grid.t_min * time_scale, grid.t_max * time_scale])
        ax.set_xlabel('Time (day)')
        if self.useCumulativePlots:
            ax.set_ylabel('Cumulative Event Count')
        else:
            ax.set_ylabel('Event Rate (#/day)')
        ax.set_title('Event Count')


def run_parallel_forecast(forecast_manager, grid, seismic_catalog, pressure_manager, wells, geologic_model,
                          forecast_name):
    forecasts = {}
    for kb, pressure in pressure_manager.active_pressure_models.items():
        forecasts[kb] = {}
        for kc, catalog in seismic_catalog.decluster_realizations():
            tmp = forecast_manager.children[forecast_name].generate_forecast_permissive(
                grid, seismic_catalog, pressure, wells, geologic_model)
            forecasts[kb][kc] = {'temporal': tmp[0], 'spatial': tmp[1], 'weight': 1.0}
    return forecasts
