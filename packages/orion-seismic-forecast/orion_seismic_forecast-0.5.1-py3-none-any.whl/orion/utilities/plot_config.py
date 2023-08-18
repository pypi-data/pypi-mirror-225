# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

from functools import partial
from orion.utilities import plot_tools
import matplotlib
from matplotlib import cm


class GUIColors():
    """
    Plot colors
    """

    def __init__(self):
        self.line_style = {'color': 'b'}

        self.alt_line_style = {'color': 'r', 'linestyle': '--'}

        self.point_style = {'color': 'b', 'marker': 'o', 'linestyle': 'None'}

        self.histogram_style = {'color': 'b', 'edgecolor': 'k'}

        self.microseismic_style = {
            'color': 'k',
            'markeredgecolor': 'k',
            'marker': 'o',
            'linestyle': 'None',
            'markersize': 3
        }

        self.well_style = {'color': 'r', 'marker': 'v', 'linestyle': 'None'}

        self.extraction_well_style = {'color': 'b', 'marker': '^', 'linestyle': 'None'}

        self.monitor_well_style = {'color': 'c', 'marker': 'd', 'linestyle': 'None'}

        self.alt_well_style = {'color': 'k', 'marker': 'v', 'linestyle': 'None'}

        self.font_size = 9
        self.map_alpha = 0.5
        self.pressure_colormap = cm.jet
        self.dpdt_colormap = cm.viridis
        self.rate_colormap = cm.cool
        self.probability_colormap = cm.hot
        self.point_colormap = cm.jet
        self.current_pressure_colormap = ''
        self.current_dpdt_colormap = ''
        self.current_rate_colormap = ''
        self.current_probability_colormap = ''
        self.current_point_colormap = ''

        self.activate_dark_mode()

    def activate_light_mode(self, theme=None):
        if theme == "sunvalley":
            self.theme = plot_tools.light_sv
            self.theme_ordered = plot_tools.light_sv_ordered

        else:
            self.theme = plot_tools.light
            self.theme_ordered = plot_tools.light_ordered

        try:
            plot_tools.registerCascadeColormap(mode='light')
            plot_tools.registerStoplightColormap()
            plot_tools.registerUSGSHazardColormap(mode='light')
            plot_tools.registerRippleColormap(mode='light')
        except:
            pass

        self.set_plot_styles()

    def activate_dark_mode(self, theme=None):
        if theme == "sunvalley":
            self.theme = plot_tools.monokai_sv
            self.theme_ordered = plot_tools.monokai_sv_ordered

        else:
            self.theme = plot_tools.monokai
            self.theme_ordered = plot_tools.monokai_ordered

        try:
            plot_tools.registerCascadeColormap(mode='dark')
            plot_tools.registerStoplightColormap()
            plot_tools.registerUSGSHazardColormap(mode='dark')
            plot_tools.registerRippleColormap(mode='dark')
        except:
            pass

        self.set_plot_styles()

    def activate_stark_mode(self):
        self.theme = plot_tools.stark
        self.theme_ordered = plot_tools.stark_ordered

        try:
            plot_tools.registerCascadeColormap(mode='light')
            plot_tools.registerStoplightColormap()
            plot_tools.registerUSGSHazardColormap(mode='light')
            plot_tools.registerRippleColormap(mode='light')
        except:
            pass

        self.set_plot_styles()
        self.microseismic_style['markeredgecolor'] = self.theme['foreground_1']

    def set_colormaps(self, pressure='cascade', dpdt='viridis', rate='hazard', probability='stoplight', point='ripple'):
        if pressure != self.current_pressure_colormap:
            self.pressure_colormap = matplotlib.colormaps.get_cmap(pressure)
            self.current_pressure_colormap = pressure

        if dpdt != self.current_dpdt_colormap:
            self.dpdt_colormap = matplotlib.colormaps.get_cmap(dpdt)
            self.current_dpdt_colormap = dpdt

        if rate != self.current_rate_colormap:
            self.rate_colormap = matplotlib.colormaps.get_cmap(rate)
            self.current_rate_colormap = rate

        if probability != self.current_probability_colormap:
            self.probability_colormap = matplotlib.colormaps.get_cmap(probability)
            self.current_probability_colormap = probability

        if point != self.current_point_colormap:
            self.point_colormap = matplotlib.colormaps.get_cmap(point)
            self.current_point_colormap = point

    def set_plot_styles(self):
        # Reset colormaps
        self.current_pressure_colormap = ''
        self.current_dpdt_colormap = ''
        self.current_rate_colormap = ''
        self.current_probability_colormap = ''
        self.current_point_colormap = ''
        self.set_colormaps()

        # Set colors
        self.point_style['color'] = self.theme['violet']
        self.microseismic_style['color'] = self.theme['foreground_0']
        self.microseismic_style['markeredgecolor'] = self.theme['background_2']
        self.well_style['color'] = self.theme['red']
        self.alt_well_style['color'] = self.theme['foreground_1']
        self.line_style['color'] = self.theme['foreground_1']
        self.alt_line_style['color'] = self.theme['red']
        self.histogram_style['color'] = self.theme['violet']
        self.periodic_line_style = partial(plot_tools.periodic_style, self.theme_ordered, ['-', '--', ':', '-.'],
                                           ['o', '*', '^', '+', 'd'])
        self.periodic_point_style = partial(plot_tools.periodic_style, self.theme_ordered, [None],
                                            ['o', '*', '^', '+', 'd'])
        self.periodic_color_style = partial(plot_tools.periodic_style, self.theme_ordered, ['-'], [None])

        matplotlib.rcParams.update({
            'font.size': str(self.font_size),
            'text.color': self.theme['foreground_1'],
            'axes.labelcolor': self.theme['foreground_1'],
            'figure.facecolor': self.theme['background_0'],
            'savefig.facecolor': self.theme['background_0'],
            'axes.facecolor': self.theme['background_0'],
            'xtick.color': self.theme['foreground_1'],
            'ytick.color': self.theme['foreground_1']
        })

    def activate_advanced_light_mode(self):
        self.activate_light_mode()

    def activate_advanced_dark_mode(self):
        self.activate_dark_mode()


gui_colors = GUIColors()
