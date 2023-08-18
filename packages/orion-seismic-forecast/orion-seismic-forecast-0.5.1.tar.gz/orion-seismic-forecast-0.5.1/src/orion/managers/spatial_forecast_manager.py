# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
spatial_forecast_manager.py
-----------------------
"""

from orion.managers import manager_base
from orion.utilities import plot_tools
from orion.utilities.plot_config import gui_colors
from orion import _frontend
import numpy as np


class SpatialForecastManager(manager_base.ManagerBase):
    """
    Spatial Forecast Plot Manager
    """

    def set_class_options(self, **kwargs):
        """
        Spatial Forecast initialization

        Args:
                config_fname (str): An optional json config file name

        """

        # Set the shorthand name
        self.short_name = 'Spatial Forecast'

    def set_user_options(self, **kwargs):
        self.catch_pressure_errors = 1
        self.spatial_slice_depth = 1.0
        self.spatial_slice_time = 1.0
        self.forecast_image_layer_options = {'Rate': 'spatial_forecast_rate', 'Count': 'spatial_forecast_count'}
        self.current_forecast_image_layer = 'Rate'

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_all()
        self.gui_elements['current_forecast_image_layer'] = {
            'element_type': 'dropdown',
            'label': 'Forecast value',
            'position': [1, 0],
            'values': list(self.forecast_image_layer_options.keys())
        }

        fig_size = (7, 6)
        if _frontend == 'strive':
            fig_size = (90, 50)

        self.figures['spatial_forecast'] = {
            'position': [0, 0],
            'layer_config': True,
            'size': fig_size,
            'extra_axis_size': (1.2, 3.2),
            'extra_axis_N': (2, 1),
            'target': 'spatial_forecast',
            'slice': ['time', 'z'],
            'figure_type': 'map_2D',
            'widgets': ['current_forecast_image_layer']
        }

    def spatial_forecast(self, plot_data):
        seismic_plot_data = plot_data['Seismic Catalog']
        well_plot_data = plot_data['Fluid Injection']
        forecast_plot_data = plot_data['Forecast Models']
        grid_plot_data = plot_data['General']

        # Trim data above the slice
        z = grid_plot_data['z'] - grid_plot_data['z_origin']
        t = grid_plot_data['t']
        t_scale = 1.0 / (60.0 * 60.0 * 24.0)
        slice_z = self.figures['spatial_forecast']['slice_values']['z']
        slice_t = self.figures['spatial_forecast']['slice_values']['time']
        zs = slice_z * (z[-1] - z[0]) + z[0]
        ts = slice_t * (t[-1] - t[0]) + t[0]
        Ia = np.where((seismic_plot_data['z'] < zs) & (seismic_plot_data['time'] < ts * t_scale))
        Ib = np.where(well_plot_data['z'] < zs)

        # Select the correct forecast data
        Ic = np.argmin(abs(t - ts))
        image_layer = self.forecast_image_layer_options[self.current_forecast_image_layer]
        unit_str = forecast_plot_data[image_layer + '_units']

        # Generate plots
        layers = {}

        if len(forecast_plot_data[image_layer]):
            sfr = np.transpose(forecast_plot_data[image_layer][Ic, ...])
            layers['Forecast'] = {
                'latitude': grid_plot_data['latitude'],
                'longitude': grid_plot_data['longitude'],
                'c': sfr,
                'type': 'image'
            }

        if Ia:
            layers['SeismicCatalog'] = {
                'latitude': seismic_plot_data['latitude'][Ia],
                'longitude': seismic_plot_data['longitude'][Ia],
                'z': seismic_plot_data['z'][Ia],
                't': {
                    'Magnitude': seismic_plot_data['magnitude'][Ia],
                    'Time (days)': seismic_plot_data['time'][Ia],
                    'Easting (m)': seismic_plot_data['x'][Ia],
                    'Northing (m)': seismic_plot_data['y'][Ia],
                },
                'type': 'scatter',
                'marker': 'circle',
                'marker_size': 3.0,
                'marker_color': 'gray'
            }

        if Ib:
            layers['Wells'] = {
                'latitude': well_plot_data['lat'][Ib],
                'longitude': well_plot_data['lon'][Ib],
                'z': well_plot_data['z'][Ib],
                't': {
                    'Well': well_plot_data['names'][Ib],
                    'Easting (m)': well_plot_data['x'][Ib],
                    'Northing (m)': well_plot_data['y'][Ib]
                },
                'type': 'scatter',
                'marker': 'circle',
                'marker_size': 4.0,
                'marker_color': 'red'
            }

        axes = {
            'c': f'Forecast ({unit_str})',
            's': 'Marker',
            'scalebar': True,
            'aspect': 'equal',
            'title': 'Forecast (t={:1.2f} days, z={:1.2f} m)'.format(ts * t_scale, zs)
        }

        return layers, axes

    def generate_plots(self, **kwargs):
        # Collect data
        grid = kwargs.get('grid')
        seismic_catalog = kwargs.get('seismic_catalog')
        wells = kwargs.get('wells')
        forecasts = kwargs.get('forecasts')
        appearance = kwargs.get('appearance')

        rate_scale = 1e6
        ts = (grid.snapshot_time * 60 * 60 * 24.0)
        Ia = np.argmin(abs(ts - grid.t))
        x_range, y_range = grid.get_plot_range()

        # Find the well locations
        well_x, well_y, well_z = wells.get_plot_location(grid)

        # Find current seismic locations
        ms_x = np.zeros(0)
        ms_y = np.zeros(0)
        ms_z = np.zeros(0)
        if seismic_catalog:
            seismic_catalog.set_slice(time_range=[-1e99, ts])
            ms_x, ms_y, ms_z = seismic_catalog.get_plot_location(grid)

        # Get the seismic forecast slices
        sf_exceedance = np.zeros((2, 2))
        sf_rate = np.zeros((2, 2))
        catalog_rate = np.zeros((2, 2))
        sf_rate_range = [0.0, 1.0]
        sf_exceedance_range = [0.0, 100.0]

        # Choose the cumulative count or rate-based estimates to plot
        target_rate_field = []
        target_catalog_field = []
        rate_units = ''
        if forecasts.use_spatial_cumulative_plots:
            rate_units = '#/km^2'
            target_rate_field = forecasts.spatial_forecast_density_count
            target_catalog_field = seismic_catalog.spatial_density_count
        else:
            rate_scale *= 60.0 * 60.0 * 24.0 * 365.25
            rate_units = '#/year*km^2'
            target_rate_field = forecasts.spatial_forecast_density_rate
            target_catalog_field = seismic_catalog.spatial_density_rate

        # Choose the plot ranges
        if seismic_catalog:
            catalog_rate = np.rot90(target_catalog_field[Ia, ...], axes=(0, 1)).copy()
            sf_rate_range = [np.nanmin(catalog_rate), np.nanmax(catalog_rate)]

        if forecasts:
            if len(forecasts.spatial_forecast_exceedance):
                sf_exceedance = np.rot90(forecasts.spatial_forecast_exceedance, axes=(0, 1))
                sf_rate = np.rot90(target_rate_field[Ia, ...], axes=(0, 1)).copy()
                if (appearance.plot_cmap_range == 'global'):
                    # sf_rate_range = [np.nanmin(target_rate_field), np.nanmax(target_rate_field)]
                    sf_rate_range[0] = min(sf_rate_range[0], np.nanmin(target_rate_field))
                    sf_rate_range[1] = max(sf_rate_range[1], np.nanmax(target_rate_field))
                else:
                    sf_exceedance_range = [np.nanmin(sf_exceedance), np.nanmax(sf_exceedance)]
                    # sf_rate_range = [np.nanmin(sf_rate), np.nanmax(sf_rate)]
                    sf_rate_range[0] = min(sf_rate_range[0], np.nanmin(sf_rate))
                    sf_rate_range[1] = max(sf_rate_range[1], np.nanmax(sf_rate))

        # Scale target values
        sf_rate *= rate_scale
        catalog_rate *= rate_scale
        sf_rate_range = np.array(sf_rate_range) * rate_scale

        # Make sure that the data ranges have a minimum size
        # so that legends render properly
        if (sf_rate_range[1] - sf_rate_range[0] < 0.1):
            sf_rate_range[1] += 0.1
        if (sf_exceedance_range[1] < 0.1):
            sf_exceedance_range[1] += 0.1

        # Setup axes
        self.logger.debug('Generating orion_manager spatial forecast plot')
        ax = self.figures['spatial_forecast']['handle'].axes[0]
        old_visibility = plot_tools.getPlotVisibility(ax)
        ax.cla()
        cfig = self.figures['spatial_forecast']['extra_axis']
        cb_ax = cfig.axes[0]
        cb_ax.cla()

        # Spatial foreacast
        probability_string = f"p(m>{forecasts.exceedance_dial_plot_magnitude:1.1f}, t<{forecasts.exceedance_plot_time_input:1.1f} days)"
        # self.logger.debug(
        #     f'exceedance range = [{sf_exceedance_range[0]:1.1f}, {sf_exceedance_range[1]:1.1f}] {probability_string}')
        ca = ax.imshow(sf_exceedance,
                       extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
                       aspect='auto',
                       interpolation='bilinear',
                       label='Probability',
                       vmin=sf_exceedance_range[0],
                       vmax=sf_exceedance_range[1],
                       cmap=gui_colors.probability_colormap,
                       visible=old_visibility['Probability'])
        plot_tools.setupColorbar(cfig, ca, cb_ax, sf_exceedance_range, probability_string)

        # Catalog spatial plot
        ax.imshow(catalog_rate,
                  extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
                  aspect='auto',
                  interpolation='bilinear',
                  label='Catalog Values',
                  vmin=sf_rate_range[0],
                  vmax=sf_rate_range[1],
                  cmap=gui_colors.rate_colormap,
                  visible=old_visibility['Catalog Values'])

        # Spatial exceedance plot
        cb_ax = self.figures['spatial_forecast']['extra_axis'].axes[1]
        cb_ax.cla()
        # self.logger.debug(
        #     f'spatial_forecast_rate range = [{sf_rate_range[0] * rate_scale:1.1e}, {sf_rate_range[1] * rate_scale:1.1e}] #/year'
        # )
        ca = ax.imshow(sf_rate,
                       extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
                       aspect='auto',
                       interpolation='bilinear',
                       label='Seismic Forecast',
                       vmin=sf_rate_range[0],
                       vmax=sf_rate_range[1],
                       cmap=gui_colors.rate_colormap,
                       visible=old_visibility['Seismic Forecast'])
        plot_tools.setupColorbar(cfig, ca, cb_ax, sf_rate_range, f'SF ({rate_units})')

        # Map layer
        plot_tools.add_basemap(ax,
                               alpha=gui_colors.map_alpha,
                               crs=grid.projection,
                               label='Map',
                               visible=old_visibility['Map'],
                               add_map=appearance.add_map_layer)

        # Add other parameters
        ax.plot(ms_x,
                ms_y,
                label='Microseismic Events',
                visible=old_visibility['Microseismic Events'],
                **gui_colors.microseismic_style)

        ax.plot(well_x, well_y, label='Wells', visible=old_visibility['Wells'], **gui_colors.well_style)

        # Set extents, labels
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_title(f'Snapshot at t = {grid.snapshot_time:1.1f} days')
        ax.legend(loc=1)
