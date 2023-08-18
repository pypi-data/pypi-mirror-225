# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
orion_manager.py
-----------------------
"""

import os
import orion
from orion.managers import manager_base
from orion.managers import list_ as managers_list
from orion.examples import built_in_manager
import logging
from orion.managers.manager_base import block_thread, recursive


class OrionManager(manager_base.ManagerBase):
    """
    Primary Orion manager class

    Args:
        config_fname (str): An optional json config file name

    Attributes:
        config_fname (str): The current config filename
        cache_root (str): Path to the user's cache directory
        cache_file (str): The cached config filename
        snapshot_time (float): Timestamp to draw plot snapshots (days)
        available_log_levels (list): The available logging options
        log_level (str): The current log level
        log_file (str): The path of the log file
        log_file_existing (str): The path to a potential pre-existing log file
        log_file_handler (logging.FileHandler): An object that writes the log to a file
        has_pressure_run (bool): A flag indicating whether pressure calculations have been completed
        permissive (bool): A flag indicating whether Orion should attempt to catch errors produced from pressure/forecast calculations

    """

    def __init__(self, **kwargs):
        orion._frontend = kwargs.get('frontend', 'tkinter')
        super().__init__(**kwargs)
        self.check_for_cache_file()
        self.load_config_file(self.config_fname)

    def set_class_options(self, **kwargs):
        """
        Setup Orion manager class options
        """
        # Set the shorthand name
        self.short_name = 'ORION'

        # Add child objects
        self.child_classes += managers_list

        # User type
        self.user_options = ['General', 'Specific Earthquake', 'Operator', 'Super User']

        # Config file
        self.config_fname = kwargs.get('config_fname', '')

        # Cache
        self.clean_start = False
        self.cache_root = os.path.expanduser('~/.cache/orion')
        self.cache_file = os.path.join(self.cache_root, 'orion_config.json')
        self.cache_file_user = os.path.join(self.cache_root, 'orion_config_user.json')
        os.makedirs(self.cache_root, exist_ok=True)

        # Log options
        self.log_level_dict = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }
        self.available_log_levels = list(self.log_level_dict.keys())
        self.log_file_existing = ''
        self.log_file_handler = None

        # Time
        self.snapshot_time = 100.0

        # Etc.
        self.N = 1
        self.has_pressure_run = False

    def set_user_options(self, **kwargs):
        self.user_type = self.user_options[0]
        self.permissive = False
        self.log_level = 'info'
        self.log_file = os.path.join(self.cache_root, 'orion_log.txt')
        self.visibility = {'Log': False}
        self.set_plot_visibility()

    def set_gui_options(self, **kwargs):
        # Gui inputs
        self.gui_elements['log_level'] = {
            'element_type': 'dropdown',
            'label': 'Log Messages',
            'position': [1, 0],
            'values': self.available_log_levels,
            'user': True
        }
        self.gui_elements['user_type'] = {
            'element_type': 'dropdown',
            'label': 'User Type',
            'position': [3, 0],
            'values': self.user_options,
            'user': True,
            'pre_update': 'frame',
            'post_update': 'frame',
            'command': self.set_plot_visibility
        }

        # Etc setup
        self.set_visibility_all()
        self.children['AppearanceManager'].apply_theme()
        self.children_with_snapshot_plots = ('SpatialForecastManager', 'PressureManager')

        # Setup figures
        if (orion._frontend == 'tkinter'):
            self.gui_elements['snapshot_time'] = {
                'element_type': 'entry',
                'label': 'Snapshot Time',
                'position': [0, 0],
                'units': '(days)'
            }

            self.gui_elements['visibility'] = {
                'element_type': 'checkbox',
                'position': [4, 0],
                'header': 'Tab Visibility:',
                'user': True
            }

            self.setup_figures(frontend='tkinter')
            plot_type = self.children['AppearanceManager'].active_plot_types
            self.setup_figure_axes(plot_type)

    def __del__(self):
        """
        Before closing, attempt to save the current
        configuration as a json file in the user's
        cache directory

        """
        try:
            self.save_all_config_files()
            self.close_figures_recursive()
        except:
            pass

    def save_all_config_files(self):
        """
        Save the user and general config files

        """
        self.logger.info('Saving config...')
        self.save_config(self.cache_file)
        self.save_config(self.cache_file_user, user=True)

    @recursive
    def process_inputs(self):
        """
        Process the log level and file location
        """
        if (self.log_file != self.log_file_existing):
            self.log_file_existing = self.log_file
            if self.log_file_handler:
                self.logger.removeHandler(self.log_file_handler)
            self.log_file_handler = logging.FileHandler(os.path.expanduser(self.log_file), mode='w', encoding='utf-8')
            self.logger.addHandler(self.log_file_handler)

        if self.log_level in self.log_level_dict:
            self.logger.setLevel(self.log_level_dict[self.log_level])
        else:
            self.logger.setLevel(logging.CRITICAL)

    def check_for_cache_file(self):
        """
        Check to see if an orion cache file is present on
        the user's machine

        """
        if not self.config_fname:
            if os.path.isfile(self.cache_file):
                self.logger.info('Resuming from cached config')
                self.config_fname = self.cache_file
            else:
                self.clean_start = True

    def save_example(self, fname):
        """
        Saves a full example in zip format

        Args:
            fname (str): Name of the target file
        """
        self.save_config(self.cache_file)
        built_in_manager.convert_config_to_example(fname, self.cache_file)

    def load_built_in(self, case_name):
        """
        Loads built in data

        Args:
            case_name (str): Name of the built-in case_name to load
        """
        os.makedirs(self.cache_root, exist_ok=True)
        built_in_manager.compile_built_in(case_name, self.cache_file)
        self.load_config_file(self.cache_file)

    def load_config_file(self, config_file):
        """
        Loads a config file

        Args:
            config_file (str): Path to the config file
        """
        self.config_fname = config_file
        self.children['SeismicCatalog'].clear_data()
        self.children['WellManager'].clear_wells()
        if self.config_fname:
            self.load_config(self.config_fname)
        self.process_inputs()

    def set_plot_visibility(self):
        """
        Update the plot visibility flag based on the copy stored on orion_manager
        """
        for v in self.children.values():
            if v.figures:
                if (self.user_type in v.visible_to_users):
                    self.visibility[v.short_name] = v.show_plots
                else:
                    self.visibility[v.short_name] = False

    def save_timelapse_figures(self, path, status=None):
        """
        Saves figures for states aligned with GridManager.t
        """
        self.logger.info('Saving baseline figures...')
        self.save_figures(path, status=status)

        self.logger.info('Saving timelapse figures...')
        N = len(self.children['GridManager'].t)
        save_legends = True
        appearance = self.children['AppearanceManager']
        for ii, t in enumerate(self.children['GridManager'].t):
            if status is not None:
                status.set(f'{ii+1}/{N}')

            self.logger.debug(f'  snapshot {ii+1}/{N} ({t})')
            self.snapshot_time = t / (60 * 60 * 24.0)
            self.generate_snapshot_plots()
            self.save_figures(path,
                              suffix=f'_{ii:04d}',
                              plot_list=self.children_with_snapshot_plots,
                              save_legends=save_legends)
            if (appearance.plot_cmap_range == 'global'):
                save_legends = False
        self.logger.info('Done!')
        if status is not None:
            status.set('')

    @block_thread
    def load_data(self, grid):
        """
        Loads data sources

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
        """
        self.process_inputs()
        if self.permissive:
            for k in self.children:
                try:
                    self.children[k].load_data(grid)
                except Exception as e:
                    print(e)
                    self.logger.warning(f'Failed to load data for {k}')
        else:
            for k in self.children:
                self.children[k].load_data(grid)

        self.children['WellDatabase'].update_well_data(self.children['GridManager'], self.children['WellManager'])

    def run(self, run_pressure=True, run_forecasts=True, status=None):
        """
        Run the Orion manager
        """
        self.logger.info('Running orion...')

        def set_status(label):
            if status:
                status.set(label)

        # Check to see if the data is loaded
        set_status('data')
        self.logger.debug('Checking to see if data is loaded')
        self.children['SeismicCatalog'].set_origin(self.children['GridManager'])
        self.load_data(self.children['GridManager'])

        # Run the key managers
        set_status('wells')
        self.children['WellManager'].calculate_well_parameters(self.children['GridManager'])

        if run_pressure:
            if status:
                status.set('pressure')
            self.logger.debug('Evaluating pressure models')
            self.children['PressureManager'].run(self.children['GridManager'], self.children['WellManager'],
                                                 self.children['GeologicModelManager'])
            self.has_pressure_run = True

        if run_forecasts:
            set_status('forecast')
            self.logger.debug('Evaluating forecast models')
            if self.has_pressure_run:
                self.children['ForecastManager'].run(self.children['GridManager'], self.children['SeismicCatalog'],
                                                     self.children['PressureManager'], self.children['WellManager'],
                                                     self.children['GeologicModelManager'])
            else:
                self.logger.warning('Pressure models must be run before forecasts are evaluated')
                self.logger.warning('Skipping forecast evaulation')

        set_status('plots')
        self.generate_all_plots()

        set_status('')
        self.logger.info('Done!')

    def get_projection(self):
        # TODO: Replace this with a TBD object from the platform
        return self.children['GridManager']

    @block_thread
    def generate_orion_plots(self, plot_list=[], **kwargs):
        """
        Generate plots for the orion manager and its children
        """
        self.logger.debug(f'Snapshot time = {self.snapshot_time:1.1f} (days)')
        self.children['GridManager'].snapshot_time = self.snapshot_time
        self.children['SeismicCatalog'].set_origin(self.children['GridManager'])
        self.update_plot_data(**self.children)

        # STRIVE plots are generated separately
        if (orion._frontend == 'strive'):
            return

        # Move priority plots to the top of the list
        priority = kwargs.get('priority')
        if priority:
            if priority in plot_list:
                plot_list.insert(0, plot_list.pop(priority.index()))

        # Render plots
        plot_objects = {
            'grid': self.children['GridManager'],
            'seismic_catalog': self.children['SeismicCatalog'],
            'pressure': self.children['PressureManager'].pressure_model,
            'wells': self.children['WellManager'],
            'forecasts': self.children['ForecastManager'],
            'appearance': self.children['AppearanceManager']
        }

        plot_objects['appearance'].setup_maps()
        for k in plot_list:
            plot_type = self.children['AppearanceManager'].active_plot_types
            self.children[k].setup_figure_axes(plot_type)
            self.children[k].generate_plots(**plot_objects)
            self.children[k].adjust_figure_axes()

    def generate_all_plots(self, **kwargs):
        """
        Generate plots for the orion manager and its children
        """
        self.logger.debug('Generating all plots')
        self.generate_orion_plots(plot_list=list(self.children.keys()), **kwargs)

    def generate_snapshot_plots(self, **kwargs):
        """
        Generate plots for the orion manager and its children
        """
        self.logger.debug('Generating snapshot plots')
        self.generate_orion_plots(plot_list=self.children_with_snapshot_plots, **kwargs)


def run_manager(config, output_dir='figures'):
    """
    Runs the orion manager without a gui

    Args:
        config (fname): File name for Orion configuration

    """
    manager = OrionManager(config_fname=config)

    # Note: there is an issue with multiprocessing + matplotlib that needs to be resolved
    #       for now, use serial processing for non-gui runs
    manager.children['ForecastManager'].use_multiprocessing = False
    manager.run()
    manager.save_figures(output_dir)
