# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
example_download_gui.py
--------------------------------------
"""

from tkinter import ttk, filedialog, IntVar, StringVar
from orion.examples import built_in_manager
from orion.gui.gui_base import GUIBase, set_relative_size
from orion.gui.custom_widgets import ScrollableFrame
from orion.utilities.plot_config import gui_colors
import logging
import threading
import queue
import webbrowser


class ExampleSelectionGUI(GUIBase):
    """
    Orion example selection gui
    """

    def __init__(self, parent):
        """
        Orion information gui initialization
        """
        # Call the parent's initialization
        super().__init__(parent.child_gui['example_selection']['window'])

        self.logger = logging.getLogger('orion_logger')

        # Gui-specific parameters
        self.parent = parent
        self.example_manager = built_in_manager.remote_examples
        self.status_size = 20

        # Examples
        self.example_container = None
        self.example_columns = 2
        self.edx_api_key = StringVar()
        self.download_path = StringVar()
        self.force_download = IntVar()
        self.example_status = {}
        for k in built_in_manager.remote_examples.available_examples.keys():
            self.example_status[k] = IntVar()

        # Threading
        self.button_request_complete = False
        self.button_request_queue = queue.Queue()
        threading.Thread(target=self.manage_button_requests, daemon=True).start()

        self.create_main()
        self.set_values()
        self.set_icon()

    def quit(self):
        """
        Close the config gui
        """
        self.update_available_built_in()
        self.example_manager.save_cache()
        self.parent.check_for_menu_examples()
        self.window.withdraw()
        self.window.destroy()
        del self.parent.child_gui['example_selection']

    def create_main(self):
        """
        Create the config gui main page
        """
        # Create the main window
        self.frame.pack(fill='both', expand=True)
        self.window.title("Example Download")
        self.window.protocol('WM_DELETE_WINDOW', self.quit)

        # Download path
        control_frame = ttk.Frame(self.frame)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        download_path_label = ttk.Label(control_frame, text="Download path")
        download_path_label.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        download_path_entry = ttk.Entry(control_frame, width=50, textvariable=self.download_path)
        download_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky='new')
        download_path_button = ttk.Button(control_frame, text=':', width=1, command=self.ask_download_path)
        download_path_button.grid(row=0, column=2, padx=5, pady=5, sticky='new')

        # EDX API
        edx_api_label = ttk.Label(control_frame, text="EDX API Key")
        edx_api_label.grid(row=1, column=0, padx=5, pady=5, sticky='new')
        edx_api_entry = ttk.Entry(control_frame, width=50, textvariable=self.edx_api_key)
        edx_api_entry.grid(row=1, column=1, padx=5, pady=5, sticky='new')
        edx_api_help_button = ttk.Button(control_frame, text='?', width=1, command=self.launch_edx_api_help)
        edx_api_help_button.grid(row=1, column=2, padx=5, pady=5, sticky='new')

        # Force Download
        force_download_label = ttk.Label(control_frame, text="Force Download?")
        force_download_label.grid(row=2, column=0, padx=5, pady=5, sticky='new')
        force_download_checkbox = ttk.Checkbutton(control_frame, variable=self.force_download)
        force_download_checkbox.grid(row=2, column=1, padx=5, pady=5, sticky='new')

        # Examples
        example_label = ttk.Label(control_frame, text="Available Examples:")
        example_label.grid(row=3, column=0, padx=5, pady=5, sticky='new')

        self.example_container = ScrollableFrame(self.frame)
        examples = sorted(built_in_manager.remote_examples.available_examples.keys())
        example_frame = self.example_container.scrollable_frame
        for ii, k in enumerate(examples):
            example_column = ii % self.example_columns
            example_row = ii // self.example_columns

            example_label = ttk.Label(example_frame, text=k)
            example_label.grid(row=example_row, column=3 * example_column, padx=5, pady=5, sticky='new')
            example_checkbox = ttk.Checkbutton(example_frame, variable=self.example_status[k])
            example_checkbox.grid(row=example_row, column=1 + 3 * example_column, padx=5, pady=5, sticky='new')

        # Add separators
        column_height = len(examples) // self.example_columns
        for ii in range(self.example_columns - 1):
            separator = ttk.Separator(example_frame, orient='vertical')
            separator.grid(row=0, column=2 + 3 * ii, rowspan=column_height, sticky='ns')

        # Grid the examples
        self.example_container.canvas.configure(bg=gui_colors.theme['background_1'], borderwidth=2, relief='sunken')
        self.example_container.grid(row=1, column=0, padx=5, pady=5, sticky='new')

        # Request
        request_button = ttk.Button(self.frame, text='Download', width=self.button_width, command=self.request_download)
        request_button.grid(row=2, column=0, padx=5, pady=5, sticky='nw')

        # Status
        self.root.update()
        x = self.frame.winfo_reqwidth() - 5
        y = self.frame.winfo_reqheight() - 8
        self.add_status(x, y, width=400)

        set_relative_size(self.frame)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)

    def ask_download_path(self):
        """
        Select the download path using a user prompt
        """
        # Ask the user for the file to save
        d = filedialog.askdirectory()
        if d:
            self.download_path.set(d)
            self.update_available_built_in()

    def launch_edx_api_help(self):
        self.parent.logger.info('Opening EDX API help page in the default browser')
        webbrowser.open(self.example_manager.edx_api_help_url)

    def set_values(self):
        """
        Set the values in the GUI
        """
        self.edx_api_key.set(self.example_manager.edx_api_key)
        self.download_path.set(self.example_manager.download_path)
        self.force_download.set(self.example_manager.force_download)
        for k in self.example_manager.available_examples.keys():
            if k in self.example_manager.current_examples:
                self.example_status[k].set(1)

    def get_values(self):
        """
        Get the values from the GUI
        """
        self.example_manager.edx_api_key = self.edx_api_key.get()
        self.example_manager.download_path = self.download_path.get()
        self.example_manager.force_download = self.force_download.get()
        self.example_manager.download_examples = []
        for k in self.example_manager.available_examples.keys():
            if self.example_status[k].get():
                self.example_manager.download_examples.append(k)

    def request_download(self):
        """
        Add a download request to the queue
        """
        self.logger.info('Requesting external data download')
        self.button_request_queue.put('download')

    def manage_button_requests(self):
        """
        Manage the request queue
        """
        while True:
            target_process = self.button_request_queue.get()
            if (target_process == 'download'):
                self.download_data()
            self.button_request_queue.task_done()

    def update_available_built_in(self):
        self.get_values()
        self.example_manager.check_data()
        self.parent.check_for_menu_examples()
        self.set_values()

    def download_data(self):
        """
        Download external data
        """
        self.get_values()
        self.example_manager.download_data(status=self.status)
        self.update_available_built_in()
