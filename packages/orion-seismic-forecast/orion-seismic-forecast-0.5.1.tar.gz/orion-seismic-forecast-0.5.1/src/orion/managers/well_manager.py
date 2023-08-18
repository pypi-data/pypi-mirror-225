# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
well_manager.py
-----------------------
"""

import numpy as np
from orion.managers import manager_base
from orion.managers import well_data
from orion.utilities.plot_config import gui_colors
from orion import _frontend
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d


class WellManager(manager_base.ManagerBase):
    """
    A class for managing well information

    Attributes:
        net_volume (np.ndarray): Cumulative fluid injection time series (at grid.t)
        net_dqdt (np.ndarray): Net fluid injection rate time series (at grid.t)
    """

    def set_class_options(self, **kwargs):
        """
        Well manager initialization
        """

        # Set the shorthand name
        self.short_name = 'Fluid Injection'

        # Add child
        # self.child_classes.append(well_data.Well)

        # Config
        self.config_type = 'unified'
        self.add_well_btn = 'Add well'
        self.remove_well_btn = 'Remove well'
        self.load_wells_btn = 'Load wells from file'

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.net_volume = np.zeros(0)
        self.net_dqdt = np.zeros(0)
        self.serial_data = []
        self.serial_names = []
        self.grid_extents = {}

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_operator()

        # Gui elements
        self.gui_elements['add_well_btn'] = {
            'element_type': 'button',
            'text': 'Add Well',
            'command': 'add_child',
            'class': well_data.Well,
            'position': [1, 0]
        }
        self.gui_elements['remove_well_btn'] = {
            'element_type': 'button',
            'text': 'Remove Well',
            'command': 'remove_child',
            'position': [1, 1]
        }
        self.gui_elements['load_wells_btn'] = {
            'element_type': 'button',
            'text': 'Load Well File',
            'command': self.load_wells_from_file,
            'position': [1, 2],
            'filetypes': [('csv', '*.csv'), ('all', '*')]
        }

        # Figures
        fig_size = (5, 3)
        if _frontend == 'strive':
            fig_size = (90, 40)

        self.figures['spatial'] = {'position': [0, 0], 'size': fig_size, 'target': 'spatial_wells'}
        self.figures['flow'] = {'position': [0, 1], 'size': fig_size, 'target': 'well_flow_rate'}
        self.figures['volume'] = {'position': [1, 0], 'size': fig_size, 'target': 'injection_volume'}
        self.figures['pressure'] = {'position': [1, 1], 'size': fig_size, 'target': 'empty_plot'}

    def add_child(self, child_name):
        """
        Adds an instance of orion.managers.well_data.Well
        when requested by the Orion Gui

        Args:
            child_name (str): Name of the new child well
        """
        self.children[child_name] = well_data.Well()

    def clear_wells(self):
        """
        Remove all wells
        """
        del self.children
        self.children = {}

    def load_data(self, grid):
        """
        Load child well data
        """
        for k in self.children:
            self.children[k].load_data(grid)
        if (len(self.children) == 0):
            self.add_child("Well")

    def load_wells_from_file(self, fname):
        self.logger.debug(f'Loading wells from file: {fname}')

        with open(fname) as f:
            for ii, line in enumerate(f):
                if (ii > 0):
                    tmp = line[:-1].split(',')
                    if (len(tmp) == 8):
                        well_name, x, y, z, init_time, flow_rate, pressure, flow_file = tmp
                        well_name = well_name.strip()
                        if well_name not in self.children.keys():
                            self.children[well_name] = well_data.Well()
                        self.children[well_name].x = float(x)
                        self.children[well_name].y = float(y)
                        self.children[well_name].z = float(z)
                        self.children[well_name].init_time = float(init_time)
                        self.children[well_name].flow_rate = float(flow_rate)
                        self.children[well_name].pressure = float(pressure)
                        self.children[well_name].fname = flow_file.strip()
                        self.children[well_name].short_name = well_name

                    else:
                        self.logger.error('Number of columns in wells file is not correct')
                        self.logger.error(
                            'Expected format includes a single-line header, comma-delimited data including:')
                        self.logger.error('well_name, x, y, z, init_time, flow_rate, pressure, flow_file')

    def calculate_well_parameters(self, grid):
        """
        Calculate well parameters

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
        """
        self.serialize_well_data(grid)
        well_names, well_x, well_y, well_z, well_lat, well_lon, well_t, well_q = self.get_well_data(grid)
        Nw = len(well_names)
        self.net_dqdt = np.zeros(len(grid.t))
        for ii in range(Nw):
            q_interp = interp1d(well_t[ii] - grid.t_origin,
                                well_q[ii],
                                bounds_error=False,
                                fill_value=(well_q[ii][0], well_q[ii][-1]))
            q_tmp = q_interp(grid.t)
            self.net_dqdt += q_tmp

        self.net_volume = cumtrapz(self.net_dqdt, grid.t, initial=0.0)

    def serialize_well_data(self, grid):
        """
        Get the serialized well data

        Returns:
            list: names, x, y, z, t, q
        """
        # Collect data
        well_names = []
        well_x = []
        well_y = []
        well_z = []
        well_lat = []
        well_lon = []
        well_t = []
        well_q = []
        for k in self.children.keys():
            well = self.children[k]
            well_names.append(well.short_name)
            well_x.append(well.x - grid.x_origin)
            well_y.append(well.y - grid.y_origin)
            well_z.append(well.z - grid.z_origin)
            well.convert_units(grid)
            well_lat.append(well.latitude)
            well_lon.append(well.longitude)
            if len(well.epoch):
                well_t.append(well.epoch)
                well_q.append(well.variable_flow_rate)
            else:
                ta = well.init_time
                well_t.append(np.array([ta - 1e10, ta - 0.001, ta, ta + 1e10]))
                well_q.append(np.array([0.0, 0.0, well.flow_rate, well.flow_rate]))

        self.serial_data = [well_names, well_x, well_y, well_z, well_lat, well_lon, well_t, well_q]
        self.serial_names = ['names', 'x', 'y', 'z', 'lat', 'lon', 't', 'q']

    def get_well_data(self, grid):
        return self.serial_data

    def get_plot_location(self, grid):
        x = []
        y = []
        if not self.serial_data:
            self.serialize_well_data(grid)
        well_names, well_x, well_y, well_z, well_lat, well_lon, well_t, well_q = self.get_well_data(grid)
        if (grid.spatial_type == 'UTM'):
            x = well_x
            y = well_y
        else:
            x = well_lon
            y = well_lat
        return np.array(x), np.array(y), np.array(well_z)

    def get_well_paths(self, grid):
        """
        Get well paths separated by nan values for plotting
        """
        path = [[] for _ in range(3)]
        offsets = [grid.x_origin, grid.y_origin, grid.z_origin]
        for well in self.children.values():
            if len(well.drill_path):
                for ii, offset in zip(range(3), offsets):
                    path[ii].append(well.drill_path[:, ii] - offset)
                    path[ii].append([np.nan])

        if len(path[0]):
            for ii in range(3):
                path[ii] = np.concatenate(path[ii], axis=0)

        return path

    def get_injector_flag(self):
        """
        Check to see if wells are on average injectors

        Returns:
            np.ndarray: array of flags indicating which wells are injectors
        """
        N = len(self.children)
        is_injector = np.zeros(N, dtype=bool)
        for ii, k in enumerate(self.children.keys()):
            well = self.children[k]
            if len(well.epoch):
                if (np.mean(well.variable_flow_rate) > 0):
                    is_injector[ii] = 1
            else:
                if (well.flow_rate > 0):
                    is_injector[ii] = 1
        return is_injector

    def get_monitor_flag(self):
        """
        Check to see if wells are monitors

        Returns:
            np.ndarray: array of flags indicating which wells are monitors
        """
        N = len(self.children)
        is_monitor = np.zeros(N, dtype=bool)
        for ii, w in enumerate(self.children.values()):
            if (w.is_monitor_well):
                is_monitor[ii] = 1
        return is_monitor

    def get_plot_data(self, projection):
        self.calculate_well_parameters(projection)
        data = {k: np.array(v) for k, v in zip(self.serial_names, self.serial_data)}
        return data

    def update_plot_data(self, **kwargs):
        grid = kwargs.get('GridManager')
        self.calculate_well_parameters(grid)
        self.grid_extents = {
            'x': [grid.x[0], grid.x[-1]],
            'y': [grid.y[0], grid.y[-1]],
            'z': [grid.z[0], grid.z[-1]],
            'lat': [grid.latitude[0], grid.latitude[-1]],
            'lon': [grid.longitude[0], grid.longitude[-1]]
        }

    def spatial_wells(self, plot_data):
        well_plot_data = plot_data['Fluid Injection']
        layers = {
            'wells': {
                'x': well_plot_data['x'],
                'y': well_plot_data['y'],
                'z': well_plot_data['z'],
                't': {
                    'Well': well_plot_data['names']
                },
                'type': 'scatter'
            }
        }
        axes = {
            'x': 'X (m)',
            'y': 'Y (m)',
        }
        return layers, axes

    def well_flow_rate(self, plot_data):
        grid_plot_data = plot_data['General']
        well_plot_data = plot_data['Fluid Injection']
        names = well_plot_data['names']
        t = well_plot_data['t']
        q = well_plot_data['q']
        Nw = len(names)
        time_scale = 1.0 / (60.0 * 60.0 * 24.0)
        ta = grid_plot_data['t'][0]

        layers = {}
        for ii in range(Nw):
            layers[names[ii]] = {'x': (t[ii] - ta) * time_scale, 'y': q[ii], 'type': 'line'}

        xr = [grid_plot_data['t'][0] * time_scale, grid_plot_data['t'][-1] * time_scale]
        axes = {'x': 'Time (days)', 'y': 'Q (m3/s)', 'x_range': xr}
        return layers, axes

    def injection_volume(self, plot_data):
        grid_plot_data = plot_data['General']
        time_scale = 1.0 / (60.0 * 60.0 * 24.0)
        xr = [grid_plot_data['t'][0] * time_scale, grid_plot_data['t'][-1] * time_scale]
        layers = {'volume': {'x': grid_plot_data['t'] * time_scale, 'y': self.net_volume * 1e-6, 'type': 'line'}}
        axes = {'x': 'Time (days)', 'y': 'Volume (m3)', 'x_range': xr}
        return layers, axes

    def generate_plots(self, **kwargs):
        """
        Generates diagnostic plots for the seismic catalog,
        fluid injection, and forecasts

        """
        # Collect data
        grid = kwargs.get('grid')
        pressure = kwargs.get('pressure')
        wells = kwargs.get('wells')

        # Setup
        max_labels = 9
        t_scale = 1.0 / (60 * 60 * 24.0)

        # Collect data
        x_range, y_range = grid.get_plot_range()
        well_names, well_x, well_y, well_z, well_lat, well_lon, well_t, well_q = self.get_well_data(grid)
        plot_x, plot_y, plot_z = self.get_plot_location(grid)
        Nw = len(well_names)

        # Location plot
        ax = self.figures['spatial']['handle'].axes[0]
        ax.cla()
        for ii in range(Nw):
            marker_style = gui_colors.periodic_point_style(ii)
            if (ii < max_labels):
                marker_style['label'] = well_names[ii]
            ax.plot(plot_x[ii], plot_y[ii], **marker_style)
        ax.set_title('Well Locations')
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        if (Nw > 0):
            ax.legend(loc=1)

        # Flow data
        ax = self.figures['flow']['handle'].axes[0]
        ax.cla()
        for ii in range(Nw):
            line_style = gui_colors.periodic_line_style(ii)
            if (ii < max_labels):
                line_style['label'] = well_names[ii]
            ax.plot((well_t[ii] - grid.t_origin) * t_scale, well_q[ii], **line_style)
        if (grid.plot_time_min < grid.plot_time_max):
            ax.set_xlim([grid.plot_time_min, grid.plot_time_max])
        else:
            ax.set_xlim([grid.t_min * t_scale, grid.t_max * t_scale])
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('Flow Rate (m3/s)')
        ax.set_title('Flow Rate')
        if (Nw > 0):
            ax.legend(loc=1)

        # Volume data
        ax = self.figures['volume']['handle'].axes[0]
        ax.cla()
        t_days = grid.t * t_scale
        if (len(self.net_volume) == len(grid.t)):
            ax.plot(t_days, self.net_volume * 1e-6, **gui_colors.line_style)
        ax.set_xlim([grid.t_min * t_scale, grid.t_max * t_scale])
        ax.set_xlabel('Time (day)')
        ax.set_ylabel(r'Net Injection $(Mm^{3})$')
        ax.set_title('Fluid Volume')

        # Pressure data
        ax = self.figures['pressure']['handle'].axes[0]
        ax.cla()
        Nm = 0
        if pressure:
            for w in wells.children.values():
                if (w.is_monitor_well):
                    G = np.meshgrid([w.x], [w.y], [w.z], grid.t, indexing='ij')
                    p = np.squeeze(pressure.p(*G))
                    Nm += 1
                    line_style = gui_colors.periodic_line_style(Nm)
                    if (Nm < max_labels):
                        line_style['label'] = w.short_name
                    ax.plot(t_days, p * 1e-6, **line_style)
        if (grid.plot_time_min < grid.plot_time_max):
            ax.set_xlim([grid.plot_time_min, grid.plot_time_max])
        else:
            ax.set_xlim([grid.t_min * t_scale, grid.t_max * t_scale])
        if (Nm > 0):
            ax.legend(loc=1)
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('Pressure (MPa)')
        ax.set_title('Pressure Monitors')
