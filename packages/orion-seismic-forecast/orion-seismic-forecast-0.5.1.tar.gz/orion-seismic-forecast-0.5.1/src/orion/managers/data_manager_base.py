"""
manager_base.py
-----------------------
"""

import json
import logging
import os
import threading
from functools import wraps
import numpy as np
from numpy.core.defchararray import encode
import h5py


def block_thread(original_fn):
    """
    Decorator that handles thread blocking
    """

    @wraps(original_fn)
    def blocked_fn(self, *xargs, **kwargs):
        with self._lock:
            return original_fn(self, *xargs, **kwargs)

    return blocked_fn


def recursive(original_fn):
    """
    Decorator that is used to apply a function recursively to itself and any children
    """

    @wraps(original_fn)
    def recursive_fn(self, *xargs, **kwargs):
        original_fn(self, *xargs, **kwargs)
        for child in self.children.values():
            child_fn = getattr(child, original_fn.__name__)
            child_fn(*xargs, **kwargs)

    return recursive_fn


class DataManagerBase():
    """
    Data manager base manager class for STRIVE

    Attributes:
        short_name (str): A short name used to be used in gui applications
        child_classes (list): A list of potential children
        children (dict): Dictionary of initialized children
        figures (dict): Dictonary to hold object plot instructions, handles
        gui_elements (dict): Dictionary of elements to be added to the gui
        cache_root (str): Location of the cache directory
        logger (self.logging.Logger): The strive logger instance
    """

    def __init__(self, **kwargs):
        """
        Generic manager initialization.  Developers should define any initialization
        behavior in the following functions:
            self.set_class_options
            self.set_user_options
            self.set_data
            self.set_gui_options

        """
        self.name = 'name'
        self._path = ''
        self.child_classes = []
        self.children = {}

        # GUI configuration
        self.gui_elements = {}
        self.figures = {}
        self._all_users = ['General', 'Super User']
        self.visible_to_users = ['Super User']

        # Cache and logging
        self.cache_root = os.path.expanduser('~/.cache/strive')
        self.logger = logging.getLogger('strive')
        logging.basicConfig(level=logging.WARNING, format='(%(asctime)s %(module)s:%(lineno)d) %(message)s')
        logging.captureWarnings(True)

        # Threading
        self._lock = threading.Lock()

        # Call user-defined setup steps
        self.set_class_options(**kwargs)
        self.initialize_children()
        self.set_user_options(**kwargs)
        self.set_data(**kwargs)
        self.set_gui_options(**kwargs)
        self.setup_figure_autowidgets()

    def set_class_options(self, **kwargs):
        """
        Setup common class options
        """
        pass

    def set_user_options(self, **kwargs):
        """
        Setup user-specific options such as color themes, fonts, etc.
        """
        pass

    def set_data(self, **kwargs):
        """
        Setup any required data structures
        """
        pass

    def set_gui_options(self, **kwargs):
        """
        Setup gui options
        """
        pass

    def __getstate__(self):
        """
        Ignore pickling certain elements
        """
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state):
        """
        Restore unpickled elements
        """
        self.__dict__.update(state)
        self.gui_elements = {}

    def initialize_children(self):
        """
        Create an instance of each object listed in child_classes
        """
        for tmp in self.child_classes:
            child = tmp()
            self.children[type(child).__name__] = child

    def add_child(self, child_name):
        """
        Method to add a new child to the current object by name

        Args:
            child_name (str): The name of the new child
        """
        self.logger.warning(f'Unrecognized child in config: {child_name}')

    def set_visibility_all(self):
        self.visible_to_users = self._all_users

    def get_projection(self):
        """
        Get projection information
        """
        return

    def get_interface_layout_recursive(self):
        """
        Convert the interface layout to a dict
        """
        layout = {'gui_elements': self.gui_elements, 'figures': self.figures, 'children': {}}

        for k, child in self.children.items():
            layout['children'][k] = child.get_interface_layout_recursive()

        return layout

    def save_interface_layout(self, fname):
        """
        Saves the manager layout as a json file

        Args:
            fname (str): Name of the target json file

        """
        layout = self.get_interface_layout_recursive()
        with open(fname, 'w') as f:
            json.dump(layout, f, indent=4)

    def get_config_recursive(self, user=False):
        """
        Convert the model configuration to a dict

        Args:
            user (bool): Flag to indicate whether to save user or general data

        """
        # Get the current level gui configs
        config = {}
        for k in self.gui_elements:
            if self.gui_elements[k].get('user', False) == user:
                config[k] = getattr(self, k)

        # Get the children's configs
        for k in self.children:
            tmp = self.children[k].get_config_recursive(user=user)
            if tmp:
                config[k] = tmp

        return config

    def pack_hdf5_file(self, fhandle, key, value):
        if isinstance(value, dict):
            fhandle.create_group(key)
            for k, v in value.items():
                self.pack_hdf5_file(fhandle[key], k, v)
        elif value is not None:
            tmp = np.array(value)
            if (tmp.dtype.kind in ['S', 'U', 'O']):
                tmp = encode(tmp)
            fhandle[key] = tmp

    def save_plot_data(self, fname):
        """
        Saves the current plot data to an hdf5 file

        Args:
            fname (str): Name of the target hdf5 file
        """
        plot_data = self.get_plot_data_recursive(self.get_projection())
        with h5py.File(fname, 'w') as f:
            for k, v in plot_data.items():
                self.pack_hdf5_file(f, k, v)

    def save_config(self, fname='', user=False):
        """
        Saves the manager config as a json file

        Args:
            fname (str): Name of the target json configuration file
            user (bool): Flag to indicate whether to save user or general data

        """
        config = self.get_config_recursive(user=user)
        with open(fname, 'w') as f:
            json.dump(config, f, indent=4)

    def set_config_recursive(self, config, ignore_attributes=['log_file']):
        """
        Sets the current object's configuration from a dictionary or json file

        Args:
            config (dict): The configuration dictionary

        """
        for k in config:
            if k in self.gui_elements:
                # Set gui element values
                try:
                    if k not in ignore_attributes:
                        if config[k] is None:
                            continue

                        # Update dict types in case of changes
                        if isinstance(config[k], dict):
                            tmp = getattr(self, k)
                            tmp.update(config[k])
                            config[k] = tmp

                        setattr(self, k, config[k])
                except KeyError:
                    self.logger.warning(f'Unrecognized parameter in configuration: {k}')

            else:
                # Set child values
                if k not in self.children:
                    self.add_child(k)
                if k in self.children:
                    self.children[k].set_config_recursive(config[k])

    def load_config(self, fname):
        """
        Loads the forecast manager config from a json file

        Args:
            fname (str): Name of the target json configuration file

        """
        self.logger.info('loading config:', fname)
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                config = json.load(f)
                self.set_config_recursive(config)

    def set_path_recursive(self, current_path=''):
        """
        Set a path string on the object, which can be used to uniquely
        identify widgets.
        """
        self._path = current_path
        for k in self.children:
            self.children[k].set_path_recursive(current_path=f'{current_path}_{k}')

    @property
    def path(self):
        return self._path

    @recursive
    def process_inputs(self):
        """
        Process any required gui inputs
        """
        pass

    @recursive
    def load_data(self, grid):
        """
        Load data into the manager
        """
        pass

    def run(self):
        """
        Run analyses
        """
        pass

    @recursive
    def get_user_variables(self):
        """
        Get user variables from the GUI
        """
        for k, v in self.gui_elements.items():
            setattr(self, k, v['variable'].value)

    @recursive
    def set_user_variables(self, grid):
        """
        Set user variables in the GUI
        """
        for k, v in self.gui_elements.items():
            v['variable'].value = getattr(self, k)

    def setup_figure_autowidgets(self):
        """
        Preprocess the figure instructions and add common autowidgets
        """
        for ka, v in self.figures.items():
            if 'slice' in v:
                v['slice_map'] = {}
                v['slice_values'] = {}
                if 'widgets' not in v:
                    v['widgets'] = []

                for kb in v['slice']:
                    autowidget_name = f'autowidget_{ka}_{kb}_value'
                    v['slice_values'][kb] = 1.0
                    v['slice_map'][kb] = autowidget_name
                    v['widgets'].append(autowidget_name)
                    setattr(self, autowidget_name, 1.0)
                    self.gui_elements[autowidget_name] = {
                        'element_type': 'slider',
                        'label': f'Slice {kb}',
                        'position': [2, 0],
                        'min': 0.0,
                        'max': 1.0,
                        'units': '(%)'
                    }

    @recursive
    def set_figures(self, frontend=''):
        """
        Open up figure handles
        """
        for k in self.figures:
            pass

    @recursive
    def update_figure_colors(self):
        """
        Update figure colors that are not set by rcParams.update()
        """
        for kb in self.figures:
            pass

    @recursive
    def close_figures(self):
        """
        Close the open figures associated with the current manager
        """
        for ka in self.figures:
            pass

    @recursive
    def generate_plots(self, **kwargs):
        """
        Generate any plots for the current object
        """
        pass

    def get_plot_data_recursive(self, projection):
        """
        Recursively collect plot data to share with other objects
        """
        # Get the plot data
        plot_data = self.get_plot_data(projection)
        if not isinstance(plot_data, dict):
            plot_data = {'value': plot_data}

        # Collect any autowidget values
        for ka, v in self.figures.items():
            for kb, kc in v.get('slice_map', {}).items():
                v['slice_values'][kb] = getattr(self, kc)

        # Get the children's configs
        for child in self.children.values():
            plot_data[child.name] = child.get_plot_data_recursive(projection)

        return plot_data

    def get_plot_data(self, projection):
        """
        Get plot data to share with other objects

        Returns:
            dict: Plot data
        """
        pass

    @recursive
    def update_plot_data(self, *xargs, **kwargs):
        """
        Update plot data for current object
        """
        pass

    @recursive
    def save_figures(self, output_path, dpi=400, plot_list=[], suffix='', save_legends=True, status=None):
        """
        Save figures

        Args:
            output_path (str): Path to place output figures
            dpi (int): Resolution of the output figures
        """
        os.makedirs(output_path, exist_ok=True)
        for k, fig in self.figures.items():
            pass

    @recursive
    def restore_defaults(self):
        """
        Process this object and its children
        """
        self.set_class_options()
        self.set_user_options()
        self.set_data()
        self.set_gui_options()

    @recursive
    def clear_data(self):
        """
        Clear any collected data
        """
        self.set_class_options()
        self.set_data()

    @recursive
    def reset_figures(self):
        """
        Reset the open figures associated with the current manager
        """
        for f in self.figures.values():
            pass
