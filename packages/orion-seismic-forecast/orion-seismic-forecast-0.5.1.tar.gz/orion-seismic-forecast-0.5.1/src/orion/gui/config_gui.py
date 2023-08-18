# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
orion_gui.py
--------------------------------------
"""

from tkinter import ttk, filedialog
# from orion.gui.custom_widgets import LabeledScale
from orion.utilities.plot_config import gui_colors
from orion.gui.gui_base import GUIBase, set_relative_size
from orion.gui.custom_widgets import CompactNotebook, ScrollableFrame
from orion.gui.gui_element_factory import add_element, element_variable_map
from functools import partial


class ConfigGUI(GUIBase):
    """
    Orion configuration gui

    Attributes:
        parent (orion.orion_gui.gui_base.GUIBase): The parent gui
        main_buttons (dict): An object to hold the control buttons in the gui
        enable_callbacks (bool): Flag to indicate whether callbacks should be enabled
        config (dict): Dict containing gui notebooks, variables, etc.
    """

    def __init__(self, parent):
        """
        Orion configuration gui initialization
        """
        # Call the parent's initialization
        super().__init__(parent.child_gui['config']['window'])

        # Gui-specific parameters
        self.parent = parent
        self.main_buttons = {}
        self.second_level_max_tabs = 50
        self.config = {'notebook': None, 'container': None, 'frame': None, 'variables': {}, 'children': {}}

        self.create_main()
        self.set_icon()
        self.enable_callbacks = True

    def quit(self):
        """
        Close the config gui
        """
        # Withdraw the window
        target_width = self.window.winfo_width()
        target_height = self.window.winfo_height()
        self.window.withdraw()
        self.update_config()
        self.window.destroy()

        # Record the latest size
        s = self.parent.orion_manager.children['AppearanceManager']
        s.config_window_size_x = target_width
        s.config_window_size_y = target_height

        # Delete the config frame
        del self.parent.child_gui['config']

    def create_main(self):
        """
        Create the config gui main page
        """
        # Create the main window
        self.frame.pack(fill='both', expand=True)
        self.window.title("Orion Model Configuration")
        self.window.protocol('WM_DELETE_WINDOW', self.quit)
        s = self.parent.orion_manager.children['AppearanceManager']
        self.set_window_size(width=s.config_window_size_x, height=s.config_window_size_y)

        # Create primary notebook
        self.config['notebook'] = CompactNotebook(self.frame)
        self.config['notebook'].grid(columnspan=4, sticky='news')
        self.config['notebook'].enable_traversal()

        # Add orion config to the first-level
        self.config['container'] = ScrollableFrame(self.config['notebook'], padding="5px")
        self.config['frame'] = self.config['container'].scrollable_frame
        self.build_config_frame(self.parent.orion_manager, self.config)
        self.config['notebook'].add(self.config['container'], text=self.parent.orion_manager.short_name)

        # Create child notebooks
        for ka, obj in self.parent.orion_manager.children.items():
            if not obj.gui_elements:
                continue

            container = ScrollableFrame(self.config['notebook'], padding="5px")
            self.config['children'][ka] = {
                'notebook': None,
                'container': container,
                'frame': container.scrollable_frame,
                'variables': {},
                'children': {}
            }
            config = self.config['children'][ka]
            self.config['notebook'].add(config['container'], text=obj.short_name)

            if obj.children:
                # Create another top-level notebook
                config['notebook'] = CompactNotebook(config['frame'])
                config['notebook'].max_short_len = 15
                config['notebook'].max_long_len = 30
                if (ka == 'WellManager'):
                    config['notebook'].max_short_len = 10

                config['notebook'].grid(row=0, column=0, columnspan=10, sticky='news')
                config['notebook'].enable_traversal()

                # Add the object config
                if (obj.config_type == 'split'):
                    config['frame'] = ttk.Frame(config['notebook'], padding="5px")
                    config['notebook'].add(config['frame'], text='main')

                self.build_config_frame(obj, config)

                # Add the children to the second-level
                for ii, kb in enumerate(obj.children.keys()):
                    if ii > self.second_level_max_tabs:
                        break

                    config['children'][kb] = {
                        'container': None,
                        'frame': ttk.Frame(config['notebook'], padding="5px"),
                        'variables': {}
                    }
                    config['notebook'].add(config['children'][kb]['frame'], text=obj.children[kb].short_name)
                    self.build_config_frame(obj.children[kb], config['children'][kb])

                # Return to the first page
                config['notebook'].select_first_tab()

            else:
                self.build_config_frame(obj, config)

        self.check_user_visibility()

        # Control buttons
        self.control_frame.pack(side="left")
        self.main_buttons['apply'] = ttk.Button(self.control_frame,
                                                text='Apply',
                                                width=self.button_width,
                                                command=self.update_config)
        self.main_buttons['save'] = ttk.Button(self.control_frame,
                                               text='Save Config',
                                               width=self.button_width,
                                               command=self.parent.save_config_interactive)
        self.main_buttons['load'] = ttk.Button(self.control_frame,
                                               text='Load Config',
                                               width=self.button_width,
                                               command=self.parent.load_config_interactive)

        # Grid main window
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.main_buttons['apply'].grid(row=0, column=0, padx=5)
        self.main_buttons['save'].grid(row=0, column=1, padx=5)
        self.main_buttons['load'].grid(row=0, column=2, padx=5)

        # Set the size
        set_relative_size(self.frame)
        set_relative_size(self.config['frame'])
        self.frame.grid_rowconfigure(1, minsize=self.control_frame_size, weight=0)

        # Return to the first page
        self.config['notebook'].select_first_tab()

        # Try setting the window size
        self.notebook_frames = {'orion': self.config}
        self.root.update()
        self.size_updater(pad_x=150, pad_y=150)

    def build_config_frame(self, parent, gui_config):
        """
        Build a config page for an Orion object

        Args:
            parent (orion.managers.manager_base.ManagerBase): The associated orion manager
            gui_config (dict): The object contaning gui elements
        """
        target_frame = gui_config['frame']
        variables = gui_config['variables']

        # Set the canvas background
        if (gui_config['container']):
            gui_config['container'].canvas.configure(bg=gui_colors.theme['background_1'], highlightthickness=0)

        # Create elements
        for kb, element in parent.gui_elements.items():
            # Add the correct variable type to the kwargs
            element['variable'] = element_variable_map[element['element_type']]()
            if element['variable'] is not None:
                variables[kb] = element['variable']

            # Setup callbacks
            target_arg_names = element.get('target_arg_names', [])
            pre_update = element.get('pre_update', False)
            command = element.get('command', None)
            filetypes = element.get('filetypes', [])
            pre_update = element.get('pre_update', '')
            post_update = element.get('post_update', '')

            # Common callbacks indicated via strings
            if isinstance(command, str):
                if (command == 'file'):
                    element['callback'] = partial(self.function_helper, parent, gui_config, element['variable'].set,
                                                  filetypes, target_arg_names, pre_update, post_update)
                elif (command == 'add_child'):
                    element['callback'] = partial(self.add_child, parent, gui_config, element['class'])

                elif (command == 'remove_child'):
                    element['callback'] = partial(self.remove_child, parent, gui_config)

                else:
                    self.logger.error(f'Unrecognized gui command: {command}')

            # Finalize callbacks
            if command is not None:
                if 'callback' not in element:
                    element['callback'] = partial(self.function_helper, parent, gui_config, command, filetypes,
                                                  target_arg_names, pre_update, post_update)
                if (element['element_type'] == 'dropdown'):
                    element['variable'].trace_add('write', element['callback'])

            # Add the element
            add_element(target_frame, parent, kb, **element)

        # Set the values
        self.set_gui_values_from_config_frame(parent, gui_config)

    def update_config_frame(self, parent, config):
        """
        Update the Orion manager with values from the current config frame

        Args:
            parent (orion.managers.manager_base.ManagerBase): The associated orion manager
            gui_config (dict): The object contaning gui elements
        """
        for kb in config['variables']:
            # Handle value conversion
            if kb in parent.gui_elements:
                current_state = ''
                try:
                    if isinstance(getattr(parent, kb), str):
                        current_state = config['variables'][kb].get()
                    elif isinstance(getattr(parent, kb), float):
                        current_state = float(config['variables'][kb].get())
                    elif isinstance(getattr(parent, kb), int):
                        current_state = int(config['variables'][kb].get())
                    else:
                        current_state = config['variables'][kb].get()

                    setattr(parent, kb, current_state)
                except ValueError:
                    self.logger.error(f'Value type changed for {kb}')

    def set_gui_values_from_config_frame(self, parent, config):
        """
        Update the Current config frame with values from the Orion manager

        Args:
            parent (orion.managers.manager_base.ManagerBase): The associated orion manager
            gui_config (dict): The object contaning gui elements
        """
        for kb in config['variables']:
            current_state = getattr(parent, kb)
            config['variables'][kb].set(current_state)

    def update_config(self):
        """
        Update all config frames with values from Orion
        """
        with self.parent.orion_manager._lock:
            self.update_config_frame(self.parent.orion_manager, self.config)
            for ka in self.parent.orion_manager.children.keys():
                if ka in self.config['children']:
                    obj = self.parent.orion_manager.children[ka]
                    config = self.config['children'][ka]
                    self.update_config_frame(obj, config)
                    if obj.children:
                        for kb in obj.children.keys():
                            if kb in config['children'].keys():
                                self.update_config_frame(obj.children[kb], config['children'][kb])
                            else:
                                # This can happen if there are too many tabs
                                self.logger.debug(f'Skipping config update for {kb}')

        # Add a data load request to the queue
        self.check_user_visibility()
        self.parent.request_data_load()

    def set_gui_values_from_config(self):
        """
        Update Orion with values from all config frames
        Also update visibility here
        """
        self.set_gui_values_from_config_frame(self.parent.orion_manager, self.config)
        for ka in self.config['children'].keys():
            obj = self.parent.orion_manager.children[ka]
            config = self.config['children'][ka]
            self.set_gui_values_from_config_frame(obj, config)
            if obj.children:
                for kb, child in obj.children.items():
                    self.set_gui_values_from_config_frame(child, config['children'][kb])

    def check_gui_children(self):
        """
        Check the Orion gui for children to add/remove
        """
        self.check_gui_children_frame(self.parent.orion_manager, self.config)

    def check_gui_children_frame(self, parent, config):
        """
        Update the current frame for children to add/remove

        Args:
            parent (orion.managers.manager_base.ManagerBase): The associated orion manager
            gui_config (dict): The object contaning gui elements
        """
        current_children = list(config['children'].keys())
        target_children = [k for k, v in parent.children.items() if v.gui_elements]

        for child_name in current_children:
            if child_name not in target_children:
                # Remove child
                config['notebook'].forget(config['children'][child_name]['frame'])
                del config['children'][child_name]

        for ii, child_name in enumerate(target_children):
            if child_name not in current_children:
                # Add child
                config['children'][child_name] = {
                    'frame': ttk.Frame(config['notebook']),
                    'variables': {},
                    'container': None
                }
                self.build_config_frame(parent.children[child_name], config['children'][child_name])
                config['notebook'].add(config['children'][child_name]['frame'], text=child_name)

            if ('children' in config['children'][child_name].keys()):
                self.check_gui_children_frame(parent.children[child_name], config['children'][child_name])

    def check_user_visibility(self):
        user_type = self.parent.orion_manager.user_type
        user_visibility = {self.parent.orion_manager.short_name: 1}
        for ka, obj in self.parent.orion_manager.children.items():
            if obj.gui_elements:
                user_visibility[obj.short_name] = int(user_type in obj.visible_to_users)

        self.config['notebook'].set_tab_visibility(user_visibility)
        # self.config['notebook'].select_first_tab()

    def function_helper(self, parent, config, target_fn, filetypes, target_arg_names, pre_update, post_update, *xargs):
        """
        Runs a function when a button is pressed.

        Args:
            parent (orion.managers.orion_manager.OrionManager) object to check for changes
            target_fn: Target function to run
            filetypes (list): List of file filters
        """
        if not self.enable_callbacks:
            return

        if (pre_update == 'frame'):
            self.update_config_frame(parent, config)
        elif (pre_update == 'all'):
            self.update_config()

        target_args = [self.parent.orion_manager.children[k] for k in target_arg_names]
        if len(filetypes):
            f = ''
            if 'folder' in filetypes:
                f = filedialog.askdirectory()
            else:
                f = filedialog.askopenfilename(filetypes=filetypes)

            if f:
                target_fn(f, *target_args)
            else:
                self.logger.warning('No file selected... skipping function call')
        else:
            target_fn(*target_args)

        self.check_gui_children()
        if (post_update == 'frame'):
            self.set_gui_values_from_config_frame(parent, config)
        elif (post_update == 'all'):
            self.set_gui_values_from_config()

        self.check_user_visibility()

    def add_child(self, parent, config, class_type):
        """
        Add a child to an orion manager

        Args:
            parent (orion.managers.manager_base.ManagerBase): The associated orion manager
            gui_config (dict): The object contaning gui elements
            class_type (object): An uninitialized orion manager subclass
        """
        if self.enable_callbacks:
            # Find the max id value for matching classes
            max_id = 0
            for ka in parent.children:
                if isinstance(parent.children[ka], class_type):
                    if ('_' in ka):
                        child_id = int(ka[ka.rfind('_') + 1:])
                        max_id = max(max_id, child_id)

            # Create an instance of the target type
            new_child = class_type()
            new_name = f'{new_child.short_name}_{max_id + 1}'
            parent.children[new_name] = new_child
            parent.children[new_name].short_name = new_name

            # Update the gui
            self.check_gui_children()

    def remove_child(self, parent, gui_config):
        """
        Remove the current child to an orion manager

        Args:
            parent (orion.managers.manager_base.ManagerBase): The associated orion manager
            gui_config (dict): The object contaning gui elements
        """
        if self.enable_callbacks:
            # Find the current selection
            current_id = gui_config['notebook'].index('current')
            short_name = gui_config['notebook'].tab(current_id)['text']

            # Search available short names
            child_name = ''
            for k, child in parent.children.items():
                if (child.short_name == short_name):
                    child_name = k

            if child_name:
                del parent.children[child_name]
                self.check_gui_children()
