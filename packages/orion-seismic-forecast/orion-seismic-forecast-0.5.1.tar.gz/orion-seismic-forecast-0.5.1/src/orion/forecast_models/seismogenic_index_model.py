# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
seismogenic_index_model.py
----------------------------
"""

import numpy as np
from orion.forecast_models import forecast_model_base
from orion.utilities import plot_tools
from orion.utilities.plot_config import gui_colors


class SeismogenicIndexModel(forecast_model_base.ForecastModel):
    """
    Seismogenic Index forecast model

    """

    def set_class_options(self, **kwargs):
        """
        Seismogenic Index model initialization

        """
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.short_name = 'SI'
        self.long_name = 'Seismogenic Index'

        # SI scaling factor
        self.scaling_factor = 20.0

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        super().set_data(**kwargs)
        self.seismogenic_index_grid = np.zeros((2, 2, 2))

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        super().set_gui_options(**kwargs)
        self.gui_elements['scaling_factor'] = {'element_type': 'entry', 'label': 'Scaling Factor', 'position': [1, 0]}

        # # Add figures
        # self.figures['seismogenic_index'] = {
        #     'position': [0, 0],
        #     'layer_config': True,
        #     'size': (7, 6),
        #     'extra_axis_size': (1.2, 3.2),
        #     'extra_axis_N': (2, 1)
        # }

    def seismogenic_index(self, event_count, dpdt, b_value, magnitude_completeness):
        """
        Seismogenic index value

        Args:
            event_count (np.ndarray): Seismicity event_count (count)
            dpdt (np.ndarray): Pressurization rate (Pa/s)
            b_value (float): Catalog b value
            magnitude_completeness (float): Magnitude of completeness for catalog

        Returns:
            np.ndarray: Seismogenic index
        """
        pr = np.cumsum(dpdt)**2
        si = np.zeros(len(event_count))
        valid_points = np.where((event_count > 1) & (dpdt > 0.0))[0]
        si[valid_points] = np.log10(event_count[valid_points]) - np.log10(
            pr[valid_points]) + b_value * magnitude_completeness
        return si

    def seismogenic_index_rate(self, dpdt, si, b_value, magnitude_completeness):
        """
        Seismogenic index value

        Args:
            dpdt (np.ndarray): Pressurization rate (Pa/s)
            si (np.ndarray): Seismogenic index value (TBD)
            b_value (float): Catalog b value
            magnitude_completeness (float): Magnitude of completeness for catalog

        Returns:
            np.ndarray: Seismogenic index rate
        """
        pr = dpdt**2
        sir = pr * 10.0**(si - (b_value * magnitude_completeness))
        return sir

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        Nx, Ny, Nz, Nt = grid.shape

        self.spatial_forecast = np.zeros((Nt, Nx, Ny))
        self.seismogenic_index_grid = np.zeros((Nt, Nx, Ny))
        b_value = seismic_catalog.b_value
        magnitude_completeness = seismic_catalog.magnitude_completeness
        dt = np.diff(grid.t)
        dt = np.concatenate([dt[:1], dt], axis=0)

        for i in range(Nx):
            for j in range(Ny):
                dpdt = pressure.dpdt_grid[i, j, 0, :]
                count = seismic_catalog.spatial_count[:, i, j]
                si = self.seismogenic_index(count, dpdt, b_value, magnitude_completeness)
                r = self.seismogenic_index_rate(dpdt, si, b_value, magnitude_completeness)

                # si_range = [np.amin(si), np.amax(si)]
                # if (si_range[1] > 0.0001):
                #     self.logger.debug(f'SI range ({i}, {j}) = ({si_range[0]}, {si_range[1]})')

                self.seismogenic_index_grid[:, i, j] = si
                self.spatial_forecast[:, i, j] = np.cumsum(r) * self.scaling_factor

        self.temporal_forecast = np.sum(self.spatial_forecast, axis=(1, 2))
        return self.temporal_forecast, self.spatial_forecast

    # def generate_plots(self, **kwargs):
    #     # Collect data
    #     grid = kwargs.get('grid')
    #     seismic_catalog = kwargs.get('seismic_catalog')
    #     wells = kwargs.get('wells')
    #     forecasts = kwargs.get('forecasts')
    #     appearance = kwargs.get('appearance')

    #     ts = (grid.snapshot_time * 60 * 60 * 24.0)
    #     Ia = np.argmin(abs(ts - grid.t))
    #     x_range, y_range = grid.get_plot_range()

    #     # Find the well locations
    #     well_x, well_y, well_z = wells.get_plot_location(grid)

    #     # Find current seismic locations
    #     ms_x = np.zeros(0)
    #     ms_y = np.zeros(0)
    #     ms_z = np.zeros(0)
    #     if seismic_catalog:
    #         seismic_catalog.set_slice(time_range=[-1e99, ts])
    #         ms_x, ms_y, ms_z = seismic_catalog.get_plot_location(grid)

    #     # Get the seismic forecast slices
    #     si = np.zeros((2, 2))
    #     si_range = [0.0, 1.0]
    #     if forecasts:
    #         if len(forecasts.spatial_forecast_exceedance):
    #             si = np.rot90(self.seismogenic_index_grid[Ia, ...], axes=(0, 1)).copy()
    #             if (appearance.plot_cmap_range == 'global'):
    #                 si_range = [np.nanmin(self.seismogenic_index_grid), np.nanmax(self.seismogenic_index_grid)]
    #             else:
    #                 si_range = [np.nanmin(si), np.nanmax(si)]

    #     # Make sure that the data ranges have a minimum size
    #     # so that legends render properly
    #     if (si_range[1] - si_range[0] < 1e-10):
    #         si_range[1] += 1

    #     # Setup axes
    #     self.logger.debug('Generating orion_manager spatial forecast plot')
    #     ax = self.figures['seismogenic_index']['handle'].axes[0]
    #     old_visibility = plot_tools.getPlotVisibility(ax)
    #     ax.cla()
    #     cfig = self.figures['seismogenic_index']['extra_axis']
    #     cb_ax = cfig.axes[0]
    #     cb_ax.cla()

    #     # Spatial forecast
    #     ca = ax.imshow(si,
    #                    extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
    #                    aspect='auto',
    #                    interpolation='bilinear',
    #                    label='SI',
    #                    vmin=si_range[0],
    #                    vmax=si_range[1],
    #                    cmap=gui_colors.rate_colormap,
    #                    visible=old_visibility['SI'])
    #     plot_tools.setupColorbar(cfig, ca, cb_ax, si_range, 'SI')

    #     # Add other parameters
    #     ax.plot(ms_x,
    #             ms_y,
    #             label='Microseismic Events',
    #             visible=old_visibility['Microseismic Events'],
    #             **gui_colors.microseismic_style)

    #     ax.plot(well_x, well_y, label='Wells', visible=old_visibility['Wells'], **gui_colors.well_style)

    #     # Set extents, labels
    #     ax_labels = grid.get_axes_labels()
    #     ax.set_xlabel(ax_labels[0])
    #     ax.set_ylabel(ax_labels[1])
    #     ax.set_xlim(x_range)
    #     ax.set_ylim(y_range)
    #     ax.set_title(f'Snapshot at t = {grid.snapshot_time:1.1f} days')
    #     ax.legend(loc=1)
