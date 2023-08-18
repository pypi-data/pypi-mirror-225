# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
seismic_catalog.py
-----------------------
"""

from orion.managers import manager_base
from orion.utilities.plot_config import gui_colors
from orion import _frontend
import numpy as np
from matplotlib.ticker import MaxNLocator


class CatalogOverviewManager(manager_base.ManagerBase):
    """
    Structure for holding 3D plot information
    """

    def set_class_options(self, **kwargs):
        """
        Seismic catalog initialization function

        """

        # Set the shorthand name
        self.short_name = 'Overview'

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_all()
        if ('no_figures' not in kwargs):
            fig_size = (10, 6)
            if _frontend == 'strive':
                fig_size = (90, 50)

            self.figures = {
                '3D_view': {
                    'position': [0, 0],
                    'size': fig_size,
                    '3D_option': True,
                    'layer_config': True,
                    'target': 'catalog_view_3D',
                    'figure_type': '3D',
                    'optional_layers': ['Seismic Catalog', 'Wells'],
                }
            }

    def catalog_view_3D(self, plot_data):
        seismic_plot_data = plot_data['Seismic Catalog']
        well_plot_data = plot_data['Fluid Injection']

        layers = {
            'Seismic Catalog': {
                'x': seismic_plot_data['x'],
                'y': seismic_plot_data['y'],
                'z': seismic_plot_data['z'],
                'c': seismic_plot_data['time'],
                's': seismic_plot_data['point_size'],
                't': {
                    'Magnitude': seismic_plot_data['magnitude']
                },
                'type': 'scatter'
            },
            'Wells': {
                'x': well_plot_data['x'],
                'y': well_plot_data['y'],
                'z': well_plot_data['z'],
                't': {
                    'Well': well_plot_data['names']
                },
                'type': 'scatter',
                'marker': 'diamond',
                'color': 'gray'
            }
        }
        axes = {'x': 'X (m)', 'y': 'Y (m)', 'z': 'Z (m)', 'c': 'Time (days)', 's': 'Marker', 'aspect': 'equal'}
        return layers, axes

    def generate_plots(self, **kwargs):
        seismic_catalog = kwargs.get('seismic_catalog')
        grid = kwargs.get('grid')
        appearance = kwargs.get('appearance')
        wells = kwargs.get('wells')
        seismic_catalog.reset_slice()

        # Get data
        t_scale = 60 * 60 * 24.0
        t = seismic_catalog.relative_time / t_scale
        magnitude = seismic_catalog.magnitude_slice
        M = len(magnitude)
        magnitude_range = [0.0, 1.0]
        if M > 0:
            magnitude_range = [np.amin(magnitude), np.amax(magnitude)]
        x_range, y_range = grid.get_plot_range()
        point_scale = 2.0
        ms_point_size = point_scale * (3**(1 + magnitude - magnitude_range[0]))
        ms_location = seismic_catalog.get_plot_location(grid)
        well_location = wells.get_plot_location(grid)
        well_paths = wells.get_well_paths(grid)

        # Check the problem dimensionality
        D = 2
        scatter_args = {}
        if appearance.active_plot_types == '3D':
            D = 3
            scatter_args['depthshade'] = 0

        # Map/3D view
        ax = self.figures['3D_view']['handle'].axes[0]
        ax.cla()
        ca = ax.scatter(*ms_location[:D],
                        s=ms_point_size,
                        c=t,
                        cmap=gui_colors.point_colormap,
                        edgecolors=gui_colors.microseismic_style['markeredgecolor'],
                        linewidths=0.5,
                        label='Catalog',
                        **scatter_args)

        # Wells
        ax.scatter(*well_location[:D], label='Wells', **gui_colors.well_style)
        ax.plot(*well_paths[:D], label='Well Path', **gui_colors.alt_line_style)

        # Colorbar
        if 'colorbar' not in self.figures['3D_view']:
            self.figures['3D_view']['colorbar'] = self.figures['3D_view']['handle'].colorbar(ca, ax=ax)
            self.figures['3D_view']['colorbar'].set_label('t (days)')
        self.figures['3D_view']['colorbar'].update_normal(ca)

        # Etc
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.set_xlim(x_range)

        ax.set_ylabel(ax_labels[1])
        ax.yaxis.set_major_locator(MaxNLocator(5))
        ax.set_ylim(y_range)

        if appearance.active_plot_types == '3D':
            ax.set_zlabel('Z (m)')
            ax.zaxis.set_major_locator(MaxNLocator(5))
            if (abs(grid.dz - 1.0) > 1e-9):
                ax.set_zlim([grid.z_max, grid.z_min])

        if (len(ms_location[0]) == 0):
            ax.set_title('(No seismic events found)')
