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

import orion
from orion.gui.gui_base import GUIBase, set_relative_size
from orion.gui.config_gui import ConfigGUI
from orion.gui.about_gui import AboutGUI
from orion.gui.example_download_gui import ExampleSelectionGUI
from orion.gui.quickstart_wizard import QuickstartWizard
from orion.gui.custom_widgets import SilentMatplotlibToolbar, CompactNotebook, ScrollableFrame, ListHandler, LabeledScale, open_link_factory
from orion.managers import orion_manager
from orion.utilities.plot_config import gui_colors
from orion.examples import built_in_manager
import ctypes
import platform
import tkinter
from tkinter import ttk, filedialog, IntVar, DoubleVar, Menu, Tk, Toplevel, Text, Scrollbar, END
from functools import partial
import logging
import threading
import queue
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.text as mpltext


class OrionGUI(GUIBase):
    """
    Main Orion gui

    Attributes:
        main_buttons (dict): An object to hold the control buttons in the gui
        notebook (orion.gui.custom_widgets.CompactNotebook): A notebook holding figure frames
        example_dropdown (tkinter.Menu): The menu holding available examples
        time_ticks (int): The number of ticks to use in the time slider
        time_slider (orion.gui.custom_widgets.LabeledScale): The primary time slider
        time_var (tkinter.DoubleVar): The time variable associated with the slider
        last_time_state (float): The time state associated with the last gui update
        last_time_range (list): The time range associated with the last gui update
        time_slider_modified (bool): A flag indicating whether the time slider has been modified
        relaunch_config (bool): A flag indicating whether the config gui should be reopened (typically following updates)
        snapshot_plots_modified (bool): A flag signaling that snapshot plots should be updated
        all_plots_modified (bool): A flag signaling that all plots should be updated
        logger (logging.Logger): The orion logging instance
        logger_frame (ttk.Frame): The frame holding the logger outputs
        logger_text (tkinter.Text): The text object holding logger outputs
        logger_index (int): The number of logging output lines
        logger_handler (orion.gui.custom_widgets.ListHandler): An object that intercepts and records logger outputs
        button_request_complete (bool): A flag signaling that button requests are complete
        button_request_queue (queue.Queue): A queue to handle button requests
        orion_manager (orion.managers.orion_manager.OrionManager): An instance of Orion
        theme (str): The active theme
    """

    def __init__(self, root, manager, profile_run=False):
        """
        Main Orion gui initialization
        """
        # Call the parent's initialization
        super().__init__(root)

        # Gui Elements
        self.main_buttons = {}
        self.notebook = None
        self.example_dropdown = None
        self.active_examples = []
        self.menus = []

        # Time slider control
        self.time_ticks = 4
        self.time_slider = None
        self.time_var = DoubleVar()
        self.last_time_state = 0.0
        self.last_time_range = [-1e50, -1e50]
        self.time_slider_modified = False
        self.time_slider_last_gui_time = 0.0
        self.time_slider_last_time = 0.0
        self.time_slider_speed_threshold = 0.2

        # Status
        self.relaunch_config = False
        self.snapshot_plots_modified = False
        self.all_plots_modified = False

        # Logging
        self.logger = logging.getLogger('orion_logger')
        logging.basicConfig(level=logging.WARNING, format='(%(asctime)s %(module)s:%(lineno)d) %(message)s')
        self.logger_frame = None
        self.logger_text = None
        self.logger_index = 0
        self.logger_messages = []
        self.logger_handler = ListHandler(self.logger_messages)
        self.logger.addHandler(self.logger_handler)

        # Threading
        self.button_request_complete = False
        self.button_request_queue = queue.Queue()
        threading.Thread(target=self.manage_button_requests, daemon=True).start()

        # Setup orion
        self.orion_manager = manager
        self.theme = self.orion_manager.children['AppearanceManager'].theme
        self.apply_theme()
        # if self.orion_manager.clean_start:
        #     for k in self.orion_manager.children['AppearanceManager']:
        #         pass

        # Initialize the forecast manager
        self.create_main()
        self.request_data_load()
        self.root.after(self.update_rate, self.updater)
        self.set_icon()

        # Set a preliminary window size, which will be updated after plots are generated
        s = self.orion_manager.children['AppearanceManager']
        if ((s.main_window_size_x > 100) & (s.main_window_size_y > 100)):
            self.set_window_size(width=s.main_window_size_x, height=s.main_window_size_y)

        # Launch the quickstart wizard on clean runs
        if self.orion_manager.clean_start:
            self.request_quickstart()

        # Profile entry point
        if profile_run:
            self.request_all()
            self.request_manual_plot_update()
            self.request_min_time_state()
            self.request_manual_plot_update()
            self.request_max_time_state()
            self.request_manual_plot_update()
            self.request_gui_quit()

    def quit(self):
        """
        Gui close method
        """
        # Record the latest size
        s = self.orion_manager.children['AppearanceManager']
        s.main_window_size_x = self.window.winfo_width()
        s.main_window_size_y = self.window.winfo_height()

        # Save the config and exit
        self.orion_manager.save_all_config_files()
        self.window.destroy()
        self.root.quit()

    def create_main(self):
        """
        Gui main window creation
        """
        # Create the main window
        self.frame.grid(padx=1, pady=1, sticky='nsew')
        self.window.title("Orion")
        self.window.protocol('WM_DELETE_WINDOW', self.quit)

        # Create menus
        gui_menu = Menu(self.frame)
        self.window.config(menu=gui_menu)

        # Files
        file_dropdown = Menu(gui_menu, tearoff=0, bd=0)
        file_dropdown.add_command(label="Save figures", command=self.request_figure_save)
        file_dropdown.add_command(label="Save timelapse", command=self.request_timelapse_save)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Quit", command=self.window.quit)
        gui_menu.add_cascade(label="File", menu=file_dropdown)

        # Config
        model_dropdown = Menu(gui_menu, tearoff=0, bd=0)
        model_dropdown.add_command(label="Configure", command=self.open_gui_config)
        model_dropdown.add_command(label="Quickstart", command=self.open_quickstart_wizard_gui)
        model_dropdown.add_command(label="Load config from file", command=self.load_config_interactive)
        model_dropdown.add_command(label="Save config to file", command=self.save_config_interactive)
        model_dropdown.add_command(label="Download Examples", command=self.open_gui_example_selection)
        gui_menu.add_cascade(label="Model", menu=model_dropdown)

        # Built-in data
        self.example_dropdown = Menu(model_dropdown, tearoff=0, bd=0)
        self.check_for_menu_examples()
        model_dropdown.add_cascade(label="Examples", menu=self.example_dropdown)

        # Help
        help_dropdown = Menu(gui_menu, tearoff=0, bd=0)
        help_dropdown.add_command(label="About Orion", command=self.open_gui_about)
        help_dropdown.add_command(label="Orion Documentation", command=open_link_factory(orion.documentation_url))
        help_dropdown.add_command(label="License", command=open_link_factory(orion.license_url))
        gui_menu.add_cascade(label="Help", menu=help_dropdown)

        # Set menu colors
        self.menus = [gui_menu, file_dropdown, model_dropdown, self.example_dropdown, help_dropdown]
        for m in self.menus:
            m.configure(background=gui_colors.theme['background_1'],
                        foreground=gui_colors.theme['foreground_0'],
                        activebackground=gui_colors.theme['background_1'],
                        activeforeground=gui_colors.theme['foreground_1'])

        # Create notebook and subframes
        self.notebook = CompactNotebook(self.frame)
        self.notebook.grid(sticky='news')
        self.build_splash_page()

        # Note: Matplotlib and Tk are sensitive to initialization order for figures
        # First open the handles
        for ka in self.orion_manager.children:
            obj = self.orion_manager.children[ka]
            if obj.figures:
                self.build_figure_frame(obj, ka)
                self.notebook.add(self.notebook_frames[ka]['container'], text=obj.short_name)

        # Next generate the figures and create the extra elements
        self.orion_manager.generate_all_plots()
        for ka in self.orion_manager.children:
            obj = self.orion_manager.children[ka]
            if obj.figures:
                self.build_figure_frame_extra_elements(obj, ka)
                self.update_figure_colors(obj, ka)

        # Control objects
        self.main_buttons['run_pressure'] = ttk.Button(self.control_frame,
                                                       text='Run Pressure',
                                                       width=self.button_width,
                                                       command=self.request_pressure)
        self.main_buttons['run_forecast'] = ttk.Button(self.control_frame,
                                                       text='Run Forecast',
                                                       width=self.button_width,
                                                       command=self.request_forecasts)
        self.main_buttons['run_all'] = ttk.Button(self.control_frame,
                                                  text='Run All',
                                                  width=self.button_width,
                                                  command=self.request_all)

        time_label = ttk.Label(self.control_frame, text='Time (days)')
        self.time_slider = LabeledScale(self.control_frame,
                                        scale_range=(0.0, 1.0),
                                        length=300,
                                        Nticks=3,
                                        variable=self.time_var,
                                        command=self.time_slider_activation,
                                        orient='horizontal')
        self.update_time_slider()
        self.time_var.set(self.orion_manager.snapshot_time)

        # Status variable
        self.status.set('')

        # Grid main window
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.control_frame.pack(side="left")
        self.main_buttons['run_pressure'].grid(row=0, column=0, padx=5)
        self.main_buttons['run_forecast'].grid(row=0, column=1, padx=5)
        self.main_buttons['run_all'].grid(row=0, column=2, padx=5)

        # Add time slider to overview window
        time_label.grid(row=0, column=3, padx=20)
        self.time_slider.grid(row=0, column=4)

        # Set the size
        set_relative_size(self.frame)
        self.frame.grid_rowconfigure(1, minsize=self.control_frame_size, weight=0)

        # Add logger page
        self.logger_frame = ttk.Frame(self.frame)
        self.logger_frame.grid(row=0, column=0, padx=5, pady=2, sticky='nsew')
        set_relative_size(self.logger_frame)
        self.notebook.add(self.logger_frame, text='Log')

        self.logger_text = Text(self.logger_frame, width=125)
        self.logger_scrollbar = Scrollbar(self.logger_frame, orient='vertical', command=self.logger_text.yview)

        self.logger_frame.grid_rowconfigure(0, weight=1)
        self.logger_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, padx=5, pady=2, sticky='nse')
        self.logger_text.grid(row=0, column=0, padx=5, pady=2, sticky='news')
        self.logger_text.config(yscrollcommand=self.logger_scrollbar.set,
                                font=('Arial', 8),
                                bg=gui_colors.theme['background_1'],
                                fg=gui_colors.theme['foreground_0'])

        # Return to the first page
        self.notebook.enable_traversal()
        self.visibility_updater()
        self.notebook.select(1)

    def build_splash_page(self):
        """
        Gui splash page creation
        """
        pass

    def check_for_menu_examples(self):
        current_examples = sorted(built_in_manager.find_built_in_files())

        for ka in self.active_examples.copy():
            if ka not in current_examples:
                ii = self.active_examples.index(ka)
                self.active_examples.pop(ii)
                self.example_dropdown.delete(ii)

        for ka in current_examples:
            self.add_example_to_menu(ka)

    def add_example_to_menu(self, example_name):
        """
        Add an example to the dropdown menu

        Args:
            example_name (str): Name of the example
        """
        if (example_name not in self.active_examples):
            self.active_examples.append(example_name)
            self.example_dropdown.add_command(label=example_name, command=partial(self.load_built_in, example_name))

    def update_figure_colors(self, parent, ka):
        """
        Update figure colors that aren't set by ttkstyle or rcParams

        Args:
            parent (orion.managers.manager_base.ManagerBase): The parent orion manager
            ka (str): The name of the orion manager used in gui definitions
        """
        objects = self.notebook_frames[ka]['objects']
        parent.update_figure_colors()
        for kb in parent.figures:
            # Navigation toolbar
            if ('static' not in parent.figures[kb]):
                toolbar = objects[kb + '_toolbar']
                toolbar.config(background=gui_colors.theme['background_1'])
                toolbar._message_label.config(background=gui_colors.theme['background_1'])
                toolbar.winfo_children()[-2].config(background=gui_colors.theme['background_1'])
                toolbar.update()

    def build_figure_frame(self, parent, ka):
        """
        Build a figure frame

        Args:
             parent (orion.managers.manager_base.ManagerBase): Associated Orion manger
             ka (str): Frame key
        """
        # Figure window
        container = ScrollableFrame(self.frame)
        container.canvas.configure(background=gui_colors.theme['background_1'], highlightthickness=0)
        self.notebook_frames[ka] = {
            'container': container,
            'frame': container.scrollable_frame,
            'objects': {},
            'sub_frames': {},
            'variables': {}
        }

        objects = self.notebook_frames[ka]['objects']
        sub_frames = self.notebook_frames[ka]['sub_frames']

        # Figure handles
        # Note: there is a bug in matplotlib that requires that these
        #       frames use the pack method instead of grid
        parent.setup_figures()
        for kb in parent.figures:
            # Add the figure
            sub_frames[kb] = ttk.Frame(self.notebook_frames[ka]['frame'])
            sub_frames[kb + '_figure'] = ttk.Frame(sub_frames[kb], style='Figure.TFrame')

            objects[kb] = FigureCanvasTkAgg(parent.figures[kb]['handle'], sub_frames[kb + '_figure'])
            objects[kb].get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

            sub_frames[kb + '_figure'].grid(row=0, column=0, rowspan=2, padx=0, pady=0)

            # Add an optional extra_axis
            if ('extra_axis' in parent.figures[kb]):
                sub_frames[kb + '_figure_extra_axis'] = ttk.Frame(sub_frames[kb], style='Figure.TFrame')

                objects[kb + '_figure_extra_axis'] = FigureCanvasTkAgg(parent.figures[kb]['extra_axis'],
                                                                       sub_frames[kb + '_figure_extra_axis'])
                objects[kb + '_figure_extra_axis'].get_tk_widget().pack()

                sub_frames[kb + '_figure_extra_axis'].grid(row=1, column=1, padx=2, pady=2, sticky='nw')

            # Grid the figure frame
            grid_xargs = {}
            for kc in ['columnspan', 'rowspan']:
                if kc in parent.figures[kb]:
                    grid_xargs[kc] = parent.figures[kb][kc]

            sub_frames[kb].grid(row=parent.figures[kb]['position'][0],
                                column=parent.figures[kb]['position'][1],
                                padx=10,
                                pady=1,
                                **grid_xargs)

    def build_figure_frame_extra_elements(self, parent, ka):
        """
        Build navigation bars and layer selection elements

        Args:
             parent (orion.managers.manager_base.ManagerBase): Associated Orion manger
             ka (str): Frame key
        """
        # Figure window
        objects = self.notebook_frames[ka]['objects']
        variables = self.notebook_frames[ka]['variables']
        sub_frames = self.notebook_frames[ka]['sub_frames']

        # Figure axes
        # Note: there is a bug in matplotlib that requires that these
        #       frames use the pack method instead of grid
        for kb in parent.figures:
            # Add the navigation toolbar
            if ('static' not in parent.figures[kb]):
                toolbar = SilentMatplotlibToolbar(objects[kb], sub_frames[kb + '_figure'])
                toolbar.update()
                place_args = {'anchor': 'sw', 'relx': 0.0, 'rely': 1.0, 'x': 0, 'y': 5}
                toolbar.place(**place_args)
                objects[kb + '_toolbar'] = toolbar

                show_command = partial(self.show_object, toolbar, place_args)
                leave_command = partial(self.hide_object, toolbar)
                leave_command(1)
                sub_frames[kb + '_figure'].bind("<Enter>", show_command)
                sub_frames[kb + '_figure'].bind("<Leave>", leave_command)

            # Add an optional layer checkbox
            if ('layer_config' in parent.figures[kb]):
                sub_frames[kb + '_config'] = ttk.Frame(sub_frames[kb], relief='sunken', borderwidth=2)
                ax = parent.figures[kb]['handle'].axes[0]

                # Get a list of candidates to add to the checkbox
                # plots = ax.get_lines() + ax.get_images()
                plots = []
                for child in ax.get_children():
                    test_label = child.get_label()
                    if test_label and not isinstance(test_label, mpltext.Text):
                        plots.append(child)
                count = 0

                for p in plots:
                    # Create a checkbutton label
                    p_name = p.get_label()
                    if p_name:
                        label = ttk.Label(sub_frames[kb + '_config'], text=p_name)
                        label.grid(row=count, column=0, sticky='nw', padx=5, pady=2)

                        # Create the variable and callback
                        variables[p_name] = IntVar()
                        variables[p_name].set(True)
                        custom_trace = function_toggle_factory(variables[p_name], parent.figures[kb]['handle'], p_name,
                                                               objects[kb])
                        variables[p_name].trace_add('write', custom_trace)

                        # Add the widget and grid
                        tmp = ttk.Checkbutton(sub_frames[kb + '_config'], variable=variables[p_name])
                        tmp.grid(row=count, column=1, padx=5, pady=5)
                        count += 1

                sub_frames[kb + '_config'].grid(row=0, column=1, padx=10, pady=(40, 0), sticky='N')

        # Set the size
        set_relative_size(self.notebook_frames[ka]['frame'])

    def time_slider_activation(self, slider_value):
        """
        Mark that the time slider has been touched

        Args:
            slider_value (float): the current slider value
        """
        self.time_slider_modified = True

    def update_time_slider(self):
        """
        Update the time slider intervals
        """
        grid_manager = self.orion_manager.children['GridManager']
        t_scale = 1.0 / (60 * 60 * 24.0)
        tmp = abs(self.last_time_range[0] - grid_manager.t_min * t_scale)
        tmp += abs(self.last_time_range[1] - grid_manager.t_max * t_scale)

        if (tmp > 1e-5):
            self.last_time_range = [grid_manager.t_min * t_scale, grid_manager.t_max * t_scale]
            self.time_slider.configure(scale_range=(grid_manager.t_min * t_scale, grid_manager.t_max * t_scale))

        self.time_var.set(self.orion_manager.snapshot_time)

    def updater(self, after=True):
        """
        Updater functions specific to the figure gui

        Args:
            after (bool): Flag to indicate whether to schedule another update
        """
        self.theme_updater()
        self.button_updater()
        self.visibility_updater()
        self.plot_updater()
        self.log_updater()
        self.size_updater()
        super().updater(after=after)

    def theme_updater(self):
        """
        This function is periodically evaluated to check for theme update requests
        """
        font_size = int(round(self.orion_manager.children['AppearanceManager'].font_size))
        font_size_figure = int(round(self.orion_manager.children['AppearanceManager'].font_size_figure))
        theme_tests = [
            self.theme != self.orion_manager.children['AppearanceManager'].theme, self.font_size != font_size,
            self.font_size_figure != font_size_figure
        ]

        if any(theme_tests):
            self.font_size = font_size
            self.font_size_figure = font_size_figure
            gui_colors.font_size = font_size_figure
            self.apply_theme(self.orion_manager.children['AppearanceManager'].theme)

            for m in self.menus:
                m.configure(background=gui_colors.theme['background_1'],
                            foreground=gui_colors.theme['foreground_0'],
                            activebackground=gui_colors.theme['background_1'],
                            activeforeground=gui_colors.theme['foreground_1'])
            self.logger_text.config(bg=gui_colors.theme['background_1'], fg=gui_colors.theme['foreground_0'])

            self.set_notebook_style()
            if ('config' in self.child_gui):
                self.child_gui['config']['frame'].set_notebook_style()

            if ('example_selection' in self.child_gui):
                self.child_gui['example_selection']['frame'].example_container.canvas.configure(
                    bg=gui_colors.theme['background_1'])

            self.orion_manager.reset_figures()
            self.orion_manager.generate_all_plots()
            for ka in self.orion_manager.children:
                obj = self.orion_manager.children[ka]
                if obj.figures:
                    self.update_figure_colors(obj, ka)

    def button_updater(self):
        """
        This function is periodically evaluated to check for button update requests
        """
        if (self.button_request_complete):
            self.update_time_slider()
            self.button_request_complete = False

    def show_object(self, target_object, place_args, cursor_state):
        """
        Callback function used to show an object when the cursor is placed over a target

        Args:
            target_object (ttk.Frame): The object to show
            place_args (dict): A list of arguments to pass to the place method
            cursor_state (bool): The state of the cursor
        """
        target_object.place(**place_args)

    def hide_object(self, target_object, cursor_state):
        """
        Callback function used to hide an object when the cursor is placed over a target

        Args:
            target_object (ttk.Frame): The object to show
            place_args (dict): A list of arguments to pass to the place method
            cursor_state (bool): The state of the cursor
        """
        target_object.place_forget()

    def plot_updater(self):
        """
        This function is periodically evaluated to check for plot update requests
        """
        if self.orion_manager.children['SeismicCatalog'].comcat_request_complete:
            self.orion_manager.generate_all_plots()
            self.update_figure_frames()
            self.orion_manager.children['SeismicCatalog'].comcat_request_complete = False

        if self.time_slider_modified:
            # Get the current states
            new_time = self.time_var.get()
            gui_time = time.time()

            # Check the current slider movement rate
            grid_manager = self.orion_manager.children['GridManager']
            t_scale = 1.0 / (60 * 60 * 24.0)
            v = (new_time - self.time_slider_last_time) / (gui_time - self.time_slider_last_gui_time)
            v /= ((grid_manager.t_max - grid_manager.t_min) * t_scale)
            self.time_slider_last_gui_time = gui_time
            self.time_slider_last_time = new_time

            if (abs(v) < self.time_slider_speed_threshold):
                # Only update if the absolute change is small
                if (abs(self.last_time_state - new_time) > 1e-4):
                    self.last_time_state = new_time
                    self.orion_manager.snapshot_time = new_time
                    self.snapshot_plots_modified = True
                self.time_slider_modified = False

        current_tab = self.notebook.get_current_tab_name()
        if self.all_plots_modified:
            self.orion_manager.generate_all_plots(priority=current_tab)
            self.update_figure_frames()
            self.all_plots_modified = False
            self.snapshot_plots_modified = False

        elif self.snapshot_plots_modified:
            self.orion_manager.generate_snapshot_plots(priority=current_tab)
            self.update_figure_frames()
            self.snapshot_plots_modified = False

    def log_updater(self):
        """
        Update the log messages in the gui
        """
        for ii in range(self.logger_index, len(self.logger_messages)):
            self.logger_text.insert(END, '%s\n' % (self.logger_messages[ii]))
            self.logger_index += 1

    def visibility_updater(self):
        """
        Set the tab visibility
        """
        self.notebook.set_tab_visibility(self.orion_manager.visibility)

    def update_figure_frames(self):
        """
        Update all figures in the gui
        """
        for ka in self.notebook_frames:
            # Redraw the figures
            for kb in self.notebook_frames[ka]['objects']:
                if ('_toolbar' not in kb):
                    self.notebook_frames[ka]['objects'][kb].draw()

    def request_data_load(self):
        """
        Add a data request load to the button request queue
        """
        self.logger.info('Requesting that data be loaded')
        self.button_request_queue.put('data')

    def request_pressure(self):
        """
        Add a pressure calculation request load to the button request queue
        """
        self.logger.info('Requesting pressure calculation')
        self.button_request_queue.put('pressure')

    def request_forecasts(self):
        """
        Add a forecast calculation request load to the button request queue
        """
        self.logger.info('Requesting forecast calculation')
        self.button_request_queue.put('forecast')

    def request_all(self):
        """
        Add a pressure/forecast calculation request load to the button request queue
        """
        self.logger.info('Requesting pressure and forecast calculations')
        self.button_request_queue.put('all')

    def request_min_time_state(self):
        """
        Add a request to the minimize the time state to the button request queue
        """
        self.logger.debug('Requesting that the time be set to minimum value')
        self.button_request_queue.put('set_min_time')

    def request_max_time_state(self):
        """
        Add a request to the maximize the time state to the button request queue
        """
        self.logger.debug('Requesting that the time be set to maximum value')
        self.button_request_queue.put('set_max_time')

    def request_manual_plot_update(self):
        """
        Add a request to manually update plots to the button request queue
        """
        self.logger.debug('Requesting a manual plot update')
        self.button_request_queue.put('update_plots')

    def request_figure_save(self):
        """
        Add a request to save figures to the button request queue
        """
        self.logger.debug('Requesting figure save')
        self.button_request_queue.put('save_figures')

    def request_timelapse_save(self):
        """
        Add a request to manually update plots to the button request queue
        """
        self.logger.debug('Requesting timelapse save')
        self.button_request_queue.put('save_timelapse')

    def request_quickstart(self):
        """
        Add a data request load to the button request queue
        """
        self.logger.info('Requesting that the quickstart be loaded')
        self.button_request_queue.put('quickstart')

    def request_gui_quit(self):
        """
        Add a request to manually update plots to the button request queue
        """
        self.logger.debug('Requesting that the gui quit')
        self.button_request_queue.put('quit')

    def manage_button_requests(self):
        """
        Manage the button request queue
        """
        while True:
            target_process = self.button_request_queue.get()
            if (target_process == 'pressure'):
                self.run_pressure()
                self.all_plots_modified = True
                self.button_request_complete = True
            elif (target_process == 'forecast'):
                self.run_forecasts()
                self.snapshot_plots_modified = True
                self.button_request_complete = True
            elif (target_process == 'all'):
                self.run_all()
                self.snapshot_plots_modified = True
                self.button_request_complete = True
            elif (target_process == 'data'):
                self.orion_manager.load_data(self.orion_manager.children['GridManager'])
                self.all_plots_modified = True
                self.button_request_complete = True
            elif (target_process == 'update_plots'):
                self.snapshot_plots_modified = True
                while self.snapshot_plots_modified:
                    time.sleep(1)
                self.button_request_complete = True
            elif (target_process == 'save_figures'):
                self.save_figures()
                self.button_request_complete = True
            elif (target_process == 'save_timelapse'):
                self.snapshot_plots_modified = True
                self.save_timelapse_figures()
                self.button_request_complete = True
            elif (target_process == 'quickstart'):
                self.open_quickstart_wizard_gui()
            elif (target_process == 'quit'):
                self.quit()
            elif ('time' in target_process):
                self.set_time(target_process)
                self.snapshot_plots_modified = True
                self.button_request_complete = True
            self.button_request_queue.task_done()

    def set_time(self, target_process):
        grid_manager = self.orion_manager.children['GridManager']
        t_scale = 1.0 / (60 * 60 * 24.0)
        if (target_process == 'set_min_time'):
            self.orion_manager.snapshot_time = grid_manager.t_min * t_scale
        elif (target_process == 'set_max_time'):
            self.orion_manager.snapshot_time = grid_manager.t_max * t_scale
        self.update_time_slider()

    def update_config(self):
        """
        Trigger an update of the orion configuration values if the config window is open
        """
        if ('config' in self.child_gui):
            self.child_gui['config']['frame'].update_config()

    def run_pressure(self):
        """
        Update the current configuration and run Orion
        """
        self.logger.info('Running pressure calculation')
        self.update_config()
        self.orion_manager.run(run_pressure=True, run_forecasts=False, status=self.status)

    def run_forecasts(self):
        """
        Update the current configuration and run Orion
        """
        self.logger.info('Running forecast calculation')
        self.update_config()
        self.orion_manager.run(run_pressure=False, run_forecasts=True, status=self.status)

    def run_all(self):
        """
        Update the current configuration and run Orion
        """
        self.logger.info('Running pressure and forecast calculations')
        self.update_config()
        self.orion_manager.run(run_pressure=True, run_forecasts=True, status=self.status)

    def pre_load_update(self):
        """
        Prepare the gui for loading a config file
        """
        if ('config' in self.child_gui):
            self.child_gui['config']['frame'].update_config()
            self.child_gui['config']['frame'].quit()
            self.relaunch_config = True
        else:
            self.relaunch_config = False

    def post_load_update(self):
        """
        Updates gui elements after loading a new config file
        """
        self.update_figure_frames()
        self.update_time_slider()

        if self.relaunch_config:
            self.open_gui_config()
            self.relaunch_config = False

    def load_built_in(self, source):
        """
        Load build in sources

        Args:
             source (str): Built in source name
        """
        self.pre_load_update()
        self.orion_manager.clear_data()
        self.orion_manager.load_built_in(source)
        self.post_load_update()

    def load_config_interactive(self):
        """
        Load a config file using a user prompt
        """
        # Ask the user for the file to save
        fname = filedialog.askopenfilename(filetypes=(("json", "*.json"), ("all", "*.*")))
        if fname:
            self.pre_load_update()
            self.orion_manager.clear_data()
            self.orion_manager.load_config_file(fname)
            self.post_load_update()

    def save_config_interactive(self):
        """
        Save the current configuration to a json file
        """
        # Update from the config window if necessary
        self.update_config()

        # Save the config
        fname = filedialog.asksaveasfilename(filetypes=(("json", "*.json"), ("zip", "*.zip"), ("all", "*.*")))
        if fname:
            if ('.zip' in fname):
                self.orion_manager.save_example(fname)
            else:
                self.orion_manager.save_config(fname)

    def save_figures(self):
        """
        Save all figures in the gui to a user-selected directory
        """
        d = filedialog.askdirectory()
        if d:
            self.logger.info('Saving figures...')
            self.orion_manager.save_figures(d, status=self.status)
            self.logger.info('Finished saving figures!')
        else:
            self.logger.warning('Figure output directory not selected')

    def save_timelapse_figures(self):
        """
        Save all figures in the gui to a user-selected directory
        """
        d = filedialog.askdirectory()
        if d:
            self.logger.info('Saving timelapse figures...')
            self.orion_manager.save_timelapse_figures(d, status=self.status)
            self.logger.info('Finished timelapse saving figures!')
        else:
            self.logger.warning('Figure output directory not selected')

    def open_gui_config(self):
        """
        Set gui configuration options
        """
        if ('config' in self.child_gui):
            self.child_gui['config']['frame'].update_config()
            self.child_gui['config']['frame'].quit()

        self.child_gui['config'] = {'window': Toplevel(self.root)}
        self.child_gui['config']['frame'] = ConfigGUI(self)

    def open_gui_example_selection(self):
        """
        Example download options
        """
        if ('example_selection' in self.child_gui):
            self.child_gui['example_selection']['frame'].quit()

        self.child_gui['example_selection'] = {'window': Toplevel(self.root)}
        self.child_gui['example_selection']['frame'] = ExampleSelectionGUI(self)

    def open_gui_about(self):
        """
        Set gui configuration options
        """
        if ('about' in self.child_gui):
            self.child_gui['about']['frame'].quit()

        self.child_gui['about'] = {'window': Toplevel(self.root)}
        self.child_gui['about']['frame'] = AboutGUI(self)

    def open_quickstart_wizard_gui(self):
        """
        Set gui configuration options
        """
        if ('Quickstart' in self.child_gui):
            self.child_gui['Quickstart']['frame'].quit()

        self.child_gui['Quickstart'] = {'window': Toplevel(self.root)}
        self.child_gui['Quickstart']['frame'] = QuickstartWizard(self, gui_name='Quickstart')


def function_toggle_factory(variable, figure, name, parent):
    """
    Function factory to handle plot visibility
    """

    def custom_callback(var_name, index, mode):
        ax = figure.axes[0]
        for child in ax.get_children():
            if (name in str(child.get_label())):
                child.set_visible(variable.get())
        parent.draw()

    return custom_callback


def launch_gui(config_fname, profile_run=False):
    """
    Launch the Orion gui

    Args:
        config_fname (str): Name of the orion config file
    """
    # Turn on windows dpi scaling
    if (platform.system() == 'Windows'):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()

    # Initialize orion
    manager = None
    try:
        manager = orion_manager.OrionManager(config_fname=config_fname, skip_data_load=True, frontend='tkinter')
    except Exception as e:
        print('Failed to load orion')
        print(e)

    # Launch the gui
    if manager:
        OrionFrame = OrionGUI(root, manager, profile_run=profile_run)
        set_relative_size(root)
        root.mainloop()


if __name__ == "__main__":
    launch_gui('')
