# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
other_settings_manager.py
--------------------------
"""

import orion
from orion.managers import manager_base
from orion.utilities import file_io
from orion.utilities.plot_config import gui_colors
from orion.managers.manager_base import recursive


class AppearanceManager(manager_base.ManagerBase):
    """
    Appearance-related settings

    Attributes:
        active_plot_types (str): The active plot type
        available_plot_types (list): The available plot types
        available_themes (list): The available color themes
        config_window_size_x (int): GUI window size along the x-dimension
        config_window_size_y (int): GUI window size along the y-dimension
        main_window_size_x (int): main GUI window size along the x-dimension
        main_window_size_y (int): main GUI window size along the y-dimension
        ms_point_size (int): The point size to use for supported plots
        theme (str): The current theme
    """

    def set_user_options(self, **kwargs):
        # Set the shorthand name
        self.short_name = 'Appearance'

        # Color mode
        self._frontend = ''
        self.available_themes = ['dark', 'light', 'stark', 'sunvalley_dark', 'sunvalley_light']
        self.theme = self.available_themes[0]

        # Color maps
        self.matplotlib_colormaps = [
            'viridis', 'plasma', 'magma', 'seismic', 'hot', 'cool', 'gray', 'spring', 'summer', 'autumn', 'winter'
        ]
        self.available_colormaps = ['hazard', 'stoplight', 'cascade', 'ripple']
        self.available_colormaps.extend(self.matplotlib_colormaps)
        self.rate_colormap = 'hazard'
        self.probability_colormap = 'stoplight'
        self.pressure_colormap = 'cascade'
        self.dpdt_colormap = 'magma'
        self.point_colormap = 'ripple'

        # Plot options
        self.plot_cmap_range_options = ['global', 'current']
        self.plot_cmap_range = self.plot_cmap_range_options[1]
        self.map_layer_alpha = 0.5
        self.ms_point_size = 1
        self.available_plot_types = ['2D', '3D']
        self.active_plot_types = self.available_plot_types[1]

        # Map options
        self.add_map_layer = True
        self.allow_self_signed_certs = False

        # Font
        self.font_size = 10.0
        self.font_size_figure = 9.0

        # Window size
        self.main_window_size_x = 1060
        self.main_window_size_y = 715
        self.config_window_size_x = 1275
        self.config_window_size_y = 620

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_all()

        # Gui inputs
        self.gui_elements['theme'] = {
            'element_type': 'dropdown',
            'label': 'Color Mode',
            'position': [0, 0],
            'values': self.available_themes,
            'user': True
        }
        self.gui_elements['plot_cmap_range'] = {
            'element_type': 'dropdown',
            'label': 'Plot range',
            'position': [1, 0],
            'values': self.plot_cmap_range_options,
            'user': True
        }

        # Color inputs
        self.gui_elements['rate_colormap'] = {
            'element_type': 'dropdown',
            'label': 'Rate colormap',
            'position': [2, 0],
            'values': self.available_colormaps,
            'user': True
        }
        self.gui_elements['probability_colormap'] = {
            'element_type': 'dropdown',
            'label': 'Probability colormap',
            'position': [2, 1],
            'values': self.available_colormaps,
            'user': True
        }
        self.gui_elements['pressure_colormap'] = {
            'element_type': 'dropdown',
            'label': 'Pressure colormap',
            'position': [3, 0],
            'values': self.available_colormaps,
            'user': True
        }
        self.gui_elements['dpdt_colormap'] = {
            'element_type': 'dropdown',
            'label': 'dpdt colormap',
            'position': [3, 1],
            'values': self.available_colormaps,
            'user': True
        }
        self.gui_elements['point_colormap'] = {
            'element_type': 'dropdown',
            'label': 'Point colormap',
            'position': [4, 0],
            'values': self.available_colormaps,
            'user': True
        }

        if orion._frontend == 'strive':
            return

        self.gui_elements['ms_point_size'] = {
            'element_type': 'entry',
            'label': 'Point size',
            'position': [4, 1],
            'user': True
        }

        # Sizes
        self.gui_elements['font_size'] = {
            'element_type': 'entry',
            'label': 'GUI Font size',
            'position': [6, 0],
            'user': True
        }
        self.gui_elements['font_size_figure'] = {
            'element_type': 'entry',
            'label': 'Figure Font size',
            'position': [6, 1],
            'user': True
        }

        self.gui_elements['main_window_size_x'] = {
            'element_type': 'entry',
            'label': 'Main Window Size',
            'position': [7, 0],
            'user': True
        }
        self.gui_elements['main_window_size_y'] = {'element_type': 'entry', 'position': [7, 1], 'user': True}
        self.gui_elements['config_window_size_x'] = {
            'element_type': 'entry',
            'label': 'Config Window Size',
            'position': [8, 0],
            'user': True
        }
        self.gui_elements['config_window_size_y'] = {'element_type': 'entry', 'position': [8, 1], 'user': True}

        # Etc
        self.gui_elements['active_plot_types'] = {
            'element_type': 'dropdown',
            'label': 'Plot types',
            'position': [9, 0],
            'values': self.available_plot_types,
            'user': True
        }
        self.gui_elements['add_map_layer'] = {
            'element_type': 'check',
            'label': 'Add map layer',
            'position': [10, 0],
            'user': True
        }
        self.gui_elements['allow_self_signed_certs'] = {
            'element_type': 'check',
            'label': 'Allow self-signed certs',
            'position': [11, 0],
            'user': True
        }

    @recursive
    def process_inputs(self):
        self.set_colormaps()

    def apply_theme(self):
        """
        Apply the theme to figures and any attached guis
        """
        if ('dark' in self.theme):
            gui_colors.activate_dark_mode()
        else:
            gui_colors.activate_light_mode()

        self.set_colormaps()

    def setup_maps(self):
        """
        Set map request options
        """
        if self.allow_self_signed_certs:
            file_io.patch_request_get()

    def set_colormaps(self):
        gui_colors.set_colormaps(pressure=self.pressure_colormap,
                                 dpdt=self.dpdt_colormap,
                                 rate=self.rate_colormap,
                                 probability=self.probability_colormap,
                                 point=self.point_colormap)
