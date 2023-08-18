# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
manager_base.py
-----------------------
"""

import os
import numpy as np
import orion
try:
    from strive import data_manager_base
    from strive.data_manager_base import recursive, block_thread
except ImportError:
    from orion.managers import data_manager_base
    from orion.managers.data_manager_base import recursive, block_thread


class ManagerBase(data_manager_base.DataManagerBase):

    def __init__(self, **kwargs):
        self.show_plots = True
        self._operator_users = ['Operator', 'Super User']
        self._plot_data = {}
        super().__init__(**kwargs)
        self.figures_require_adjustment = True
        self.name = self.short_name
        self.config_type = 'split'

    def __getstate__(self):
        """
        Ignore pickling certain elements
        """
        state = self.__dict__.copy()
        del state["gui_elements"]
        del state["_lock"]
        del state["_plot_data"]
        return state

    def set_visibility_operator(self):
        self.visible_to_users = self._operator_users.copy()

    @data_manager_base.recursive
    def setup_figures(self, frontend=''):
        """
        Open up figure handles
        """
        if orion._frontend == 'strive':
            return

        from matplotlib.figure import Figure
        import matplotlib.pyplot as plt
        try:
            from mpl_toolkits.mplot3d import Axes3D
        except:
            pass

        for k in self.figures:
            if ('handle' not in self.figures[k]):
                if frontend:
                    self.figures[k]['handle'] = Figure(figsize=self.figures[k]['size'], dpi=100)
                else:
                    self.figures[k]['handle'] = plt.figure(figsize=self.figures[k]['size'], dpi=100)
                self.figures[k]['create_axes'] = True

            if ('extra_axis_size' in self.figures[k]):
                if ('extra_axis' not in self.figures[k]):
                    if frontend:
                        self.figures[k]['extra_axis'] = Figure(figsize=self.figures[k]['extra_axis_size'], dpi=100)
                    else:
                        self.figures[k]['extra_axis'] = plt.figure(figsize=self.figures[k]['extra_axis_size'], dpi=100)

    @data_manager_base.recursive
    def reset_figures(self):
        """
        Reset the open figures associated with the current manager
        """
        if orion._frontend == 'strive':
            return

        for f in self.figures.values():
            f['create_axes'] = True
            f['handle'].clf()
            if ('extra_axis_size' in f):
                f['extra_axis'].clf()

            if ('colorbar' in f):
                del f['colorbar']

    @data_manager_base.recursive
    def close_figures(self):
        """
        Close the open figures associated with the current manager
        """
        if orion._frontend == 'strive':
            return

        for ka in self.figures:
            for kb in ['handle', 'extra_axis']:
                if (kb in self.figures[ka]):
                    del self.figures[ka][kb]

    @data_manager_base.recursive
    def setup_figure_axes(self, plot_type):
        """
        Setup any requested figure axes for the current object

        Args:
            plot_type (str): The target dimension for supported plots (2D or 3D)
        """
        if orion._frontend == 'strive':
            return

        for k in self.figures:
            if self.figures[k]['create_axes']:
                self.figures[k]['max_dimension'] = plot_type
                self.figures[k]['create_axes'] = False
                if ('N' in self.figures[k]):
                    N = self.figures[k]['N']
                    for ii in range(N[0] * N[1]):
                        self.figures[k]['handle'].add_subplot(N[0], N[1], ii + 1)
                else:
                    if (('3D_option' in self.figures[k]) and (plot_type == '3D')):
                        self.figures[k]['handle'].add_subplot(1, 1, 1, projection='3d')
                        self.figures[k]['current_dimension'] = '3D'
                    else:
                        self.figures[k]['handle'].add_subplot(1, 1, 1)
                        self.figures[k]['current_dimension'] = '2D'

                if ('extra_axis_size' in self.figures[k]):
                    if ('extra_axis_N' in self.figures[k]):
                        N = self.figures[k]['extra_axis_N']
                        for ii in range(N[0] * N[1]):
                            self.figures[k]['extra_axis'].add_subplot(N[0], N[1], ii + 1)
                    else:
                        self.figures[k]['extra_axis'].add_subplot(1, 1, 1)

        # Check to see if the figure axes match the expected dimensions
        regenerate_axes = False
        for k in self.figures:
            if (plot_type != self.figures[k]['max_dimension']):
                if ('3D_option' in self.figures[k]):
                    regenerate_axes = True

        if regenerate_axes:
            self.reset_figures()
            self.setup_figure_axes(plot_type)
            self.update_figure_colors()

    def update_figure_colors(self):
        """
        Update figure colors that are not set by rcParams.update()
        """
        if orion._frontend == 'strive':
            return

        from orion.utilities.plot_config import gui_colors
        from PIL import ImageColor

        for kb in self.figures:
            # Main figure
            self.figures[kb]['handle'].patch.set_facecolor(gui_colors.theme['background_1'])

            if self.figures[kb].get('current_dimension', '2D') == '3D':
                ax = self.figures[kb]['handle'].axes[0]
                ax.set_facecolor(gui_colors.theme['background_1'])
                rgb = ImageColor.getcolor(gui_colors.theme['foreground_0'], "RGB")
                axis_color = (rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0, 0.0)
                ax.w_xaxis.set_pane_color(axis_color)
                ax.w_yaxis.set_pane_color(axis_color)
                ax.w_zaxis.set_pane_color(axis_color)

            # Extra_axis
            if ('extra_axis' in self.figures[kb]):
                self.figures[kb]['extra_axis'].patch.set_facecolor(gui_colors.theme['background_1'])

    def adjust_figure_axes(self):
        """
        Apply formatting to the figures on the current object
        """
        if orion._frontend == 'strive':
            return

        if self.figures_require_adjustment:
            self.figures_require_adjustment = False
        else:
            return

        for k in self.figures:
            try:
                self.figures[k]['handle'].tight_layout()
            except:
                pass

            if ('extra_axis' in self.figures[k]):
                try:
                    self.figures[k]['extra_axis'].tight_layout()
                except:
                    pass

    def save_figures(self, output_path, dpi=400, plot_list=[], suffix='', save_legends=True, status=None):
        """
        Save figures

        Args:
            output_path (str): Path to place output figures
            dpi (int): Resolution of the output figures
        """
        if orion._frontend == 'strive':
            return

        if status is not None:
            status.set('Rendering figures')

        os.makedirs(output_path, exist_ok=True)
        for k, fig in self.figures.items():
            fig['handle'].savefig(os.path.join(output_path, f'{k}{suffix}.png'), dpi=dpi)
            if (('extra_axis' in fig) and save_legends):
                fig['extra_axis'].savefig(os.path.join(output_path, f'legend_{k}{suffix}.png'), dpi=dpi)

        # Save child object figures
        for k in self.children:
            if (len(plot_list) == 0) or (k in plot_list):
                self.children[k].save_figures(output_path, suffix=suffix, save_legends=save_legends)

        if status is not None:
            status.set('')

    def empty_plot(self, plot_data):
        layers = {'empty': {'x': np.zeros(0), 'y': np.zeros(0), 'type': 'scatter'}}
        axes = {'x': 'X (m)', 'y': 'Y (m)'}
        return layers, axes
