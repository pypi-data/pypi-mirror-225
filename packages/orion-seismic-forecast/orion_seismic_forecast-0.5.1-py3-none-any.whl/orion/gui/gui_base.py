# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
gui_base.py
--------------------------------------
"""

import logging
from tkinter import ttk, font, StringVar
from orion.utilities.plot_config import gui_colors
import os
from PIL import Image, ImageTk
import matplotlib

matplotlib.use("TkAgg")


class GUIBase():
    """
    Orion Gui base class

    Attributes:
        root (Tk.root): The root gui instance
        frame (ttk.Frame): The frame holding gui contents
        control_frame (ttk.Frame): The frame holding gui control objects
        control_frame_size (int): The minimum height for the control frame
        notebook_frames (dict): A dict holding frames placed in the notebook and their children
        window (ttk.Frame.master): The handle for the gui frame
        button_width (int): The default width of control buttons
        child_gui (dict): A dict containing handles for child gui objects
        theme (str): The active color theme (dark, light)
        update_size (bool): A flag to indicate whether the window should be resized
        update_rate (int): The update frequency for the gui (milliseconds)
        status (tkinter.StringVar): A variable holding short status information to display in the gui
        status_label (tkinter.StringVar): A variable holding the active status
        status_value (str): The contents of the status variable
        preferred_built_in (list): A list of built-in themes to use if available
        gui_source_path (str): The path to the gui scripts
    """

    def __init__(self, root):
        """
        Orion gui base class initialization
        """
        self.root = root
        self.frame = ttk.Frame(root)
        self.bottom_frame = ttk.Frame(self.frame)
        self.control_frame = ttk.Frame(self.bottom_frame, padding="5px")
        self.control_frame_size = 55
        self.notebook_frames = {}
        self.window = self.frame.master
        self.button_width = 15
        self.child_gui = {}
        self.theme = 'dark'

        self.font_preference_order = ['DejaVu Sans', 'helvetica']
        self.font_name = None
        self.font_size = 10
        self.font_size_figure = 9

        # Logging
        self.logger = logging.getLogger('orion_logger')
        logging.basicConfig(level=logging.WARNING, format='(%(asctime)s %(module)s:%(lineno)d) %(message)s')

        # Status
        self.enable_callbacks = False
        self.update_size = True
        self.update_rate = 1000
        self.status_spin = 0
        self.status_size = 9
        self.status = StringVar()
        self.status_label = StringVar()
        self.status_value = ''
        self.status.trace_add('write', self.set_status)

        # self.preferred_built_in = ['vista', 'aqua']
        self.preferred_built_in = []
        self.gui_source_path = os.path.split(__file__)[0]

    def destroy(self):
        """
        Destroy the current gui
        """
        self.window.destroy()

    def set_window_size(self, width=1060, height=715):
        """
        Set the window size

        Args:
            width (int): The target window width
            height (int): The target window height
        """
        self.root.geometry('%ix%i' % (width, height))

    def lift(self):
        self.root.lift()

    def set_icon(self):
        """
        Set the gui icon
        """
        icon_path = os.path.join(self.gui_source_path, 'smart_orb.png')
        icon = ImageTk.PhotoImage(Image.open(icon_path))
        self.root.iconphoto(False, icon)

    def apply_theme(self, theme=''):
        """
        Set the gui theme

        Args:
            theme (str): The target theme (dark, light)
        """
        import sv_ttk

        if theme:
            self.theme = theme
        theme_split = self.theme.split('_')

        available_fonts = font.families()
        for k in self.font_preference_order:
            if k in available_fonts:
                self.font_name = k
                break

        # Sunvalley themes
        if theme_split[0] == 'sunvalley':
            try:
                sv_ttk.set_theme(theme_split[1])
                if theme_split[1] == "dark":
                    gui_colors.activate_dark_mode(theme="sunvalley")
                else:
                    gui_colors.activate_light_mode(theme="sunvalley")

                ttkstyle = ttk.Style()
                self.BasicFont = font.Font(family=self.font_name, size=self.font_size, weight='normal', slant='roman')
                self.HighlightFont = font.Font(family=self.font_name,
                                               size=self.font_size,
                                               weight='bold',
                                               slant='italic')
                self.HighlightFont2 = font.Font(family=self.font_name,
                                                size=self.font_size,
                                                weight='normal',
                                                slant='italic')
                ttkstyle.configure('.', font=self.BasicFont)

            except Exception as e:
                self.logger.debug(f'Could not load advanced theme ({e})')
                self.logger.debug('Loading the backup theme instead')
                theme_split[0] = 'backup'

        # Backup themes
        if theme_split[0] != 'sunvalley':
            built_in_theme = 'clam'
            available_styles = ttk.Style().theme_names()
            for k in available_styles:
                if k in self.preferred_built_in:
                    built_in_theme = k

            # Set theme colors
            ttkstyle = ttk.Style()
            ttkstyle.theme_use(built_in_theme)
            if (theme_split[-1] == 'dark'):
                gui_colors.activate_dark_mode()
            elif (theme_split[-1] == 'light'):
                gui_colors.activate_light_mode()
            else:
                gui_colors.activate_stark_mode()

            self.BasicFont = font.Font(family=self.font_name, size=self.font_size, weight='normal', slant='roman')
            self.HighlightFont = font.Font(family=self.font_name, size=self.font_size, weight='bold', slant='italic')
            self.HighlightFont2 = font.Font(family=self.font_name, size=self.font_size, weight='normal', slant='italic')
            ttkstyle.configure('.', font=self.BasicFont)

            self.window.configure(background=gui_colors.theme['background_0'])

            ttkstyle.configure('TFrame', background=gui_colors.theme['background_1'])

            ttkstyle.configure('TButton',
                               padding=1,
                               background=gui_colors.theme['background_1'],
                               foreground=gui_colors.theme['foreground_0'],
                               bordercolor=gui_colors.theme['background_0'])
            ttkstyle.map('TButton',
                         background=[("pressed", gui_colors.theme['background_0']),
                                     ('active', gui_colors.theme['background_1'])],
                         foreground=[("pressed", gui_colors.theme['foreground_0']),
                                     ('active', gui_colors.theme['foreground_1'])])

            ttkstyle.configure('TLabel',
                               padding=4,
                               background=gui_colors.theme['background_1'],
                               foreground=gui_colors.theme['foreground_0'])

            ttkstyle.configure('TNotebook',
                               background=gui_colors.theme['background_1'],
                               foreground=gui_colors.theme['foreground_0'])

            ttkstyle.map("TNotebook.Tab",
                         background=[('selected', gui_colors.theme['background_1']),
                                     ('active', gui_colors.theme['background_0']),
                                     ("!disabled", gui_colors.theme['background_0'])],
                         foreground=[('selected', gui_colors.theme['foreground_0']),
                                     ('active', gui_colors.theme['foreground_0']),
                                     ("!disabled", gui_colors.theme['foreground_1'])])

            ttkstyle.configure('TCheckbutton',
                               padding=2,
                               indicatorbackground=gui_colors.theme['background_0'],
                               indicatorforeground=gui_colors.theme['foreground_1'])
            ttkstyle.map("TCheckbutton",
                         background=[("!disabled", gui_colors.theme['background_1'])],
                         foreground=[("!disabled", gui_colors.theme['background_0'])])

            ttkstyle.configure('TScale',
                               padding=2,
                               background=gui_colors.theme['background_1'],
                               foreground=gui_colors.theme['foreground_0'],
                               troughcolor=gui_colors.theme['background_0'])

            ttkstyle.configure('TCombobox',
                               padding=2,
                               background=gui_colors.theme['background_2'],
                               foreground=gui_colors.theme['foreground_0'],
                               fieldbackground=gui_colors.theme['background_0'])

            # The combobox dropdown requires a different method to change colors:
            self.root.option_add('*TCombobox*Listbox*Background', gui_colors.theme['background_1'])
            self.root.option_add('*TCombobox*Listbox*Foreground', gui_colors.theme['foreground_0'])
            self.root.option_add('*TCombobox*Listbox*selectBackground', gui_colors.theme['background_1'])
            self.root.option_add('*TCombobox*Listbox*selectForeground', gui_colors.theme['foreground_1'])

            ttkstyle.configure('TEntry',
                               padding=2,
                               background=gui_colors.theme['background_0'],
                               foreground=gui_colors.theme['foreground_0'],
                               fieldbackground=gui_colors.theme['background_0'],
                               insertcolor=gui_colors.theme['foreground_0'])
            ttkstyle.map('TEntry',
                         selectbackground=[('!disabled', gui_colors.theme['violet'])],
                         selectforeground=[('!disabled', gui_colors.theme['background_0'])])

            ttkstyle.configure('TText',
                               padding=2,
                               highlightbackground=gui_colors.theme['background_0'],
                               highlightforeground=gui_colors.theme['foreground_0'])
            ttkstyle.map('TText',
                         selectbackground=[('!disabled', gui_colors.theme['violet'])],
                         selectforeground=[('!disabled', gui_colors.theme['background_0'])])

    def set_tab_style(self, target):
        """
        Update the style of objects in the current tab not effected by ttkstyle

        Args:
            target (dict): A dict holding tab definitions
        """
        if ('container' in target.keys()):
            if (target['container']):
                target['container'].canvas.configure(background=gui_colors.theme['background_1'])

    def set_tab_style_recursive(self, target):
        """
        Recursively update the style of objects in the current tab not effected by ttkstyle

        Args:
            target (dict): A dict holding tab definitions
        """
        self.set_tab_style(target)
        if ('children' in target.keys()):
            for child in target['children'].values():
                self.set_tab_style_recursive(child)

    def set_notebook_style(self):
        """
        Update the style of objects in the notebook not effected by ttkstyle
        """
        for tab in self.notebook_frames.values():
            self.set_tab_style_recursive(tab)

    def add_status(self, x, y, height=30, width=140):
        """
        Add a status label to the target gui

        Args:
            x (int): The x-position of the status label
            y (int): The y-position of the status label
        """
        status_label = ttk.Label(self.bottom_frame, textvariable=self.status_label)
        status_label.pack(side="right", padx=10.0)

    def get_frame_size_recursive(self, target):
        """
        Get the natural sizes of the frames and their children

        Args:
            target (dict): A dict holding tab definitions
        """
        target_height = target['frame'].winfo_reqheight()
        target_width = target['frame'].winfo_reqwidth()
        if ('children' in target):
            for child in target['children'].values():
                child_height, child_width = self.get_frame_size_recursive(child)
                target_height = max(target_height, child_height)
                target_width = max(target_width, child_width)
        return target_height, target_width

    def get_frame_size(self, target):
        """
        Get the natural sizes of the target frame

        Args:
            target (dict): A dict holding tab definitions
        """
        target_height = 0
        target_width = 0
        for k, child in target.items():
            child_height, child_width = self.get_frame_size_recursive(child)
            target_height = max(target_height, child_height)
            target_width = max(target_width, child_width)
        return target_height, target_width

    def size_updater(self, pad_x=20, pad_y=150):
        """
        This function is periodically evaluated to check for gui size update requests

        Args:
            pad_x (int): The amount to pad the window in the x-direction
            pad_y (int): The amount to pad the window in the y-direction
        """
        if self.update_size:
            # Note: the dpi scaling applied to figures requires a
            # different target window size on windows systems
            target_height, target_width = self.get_frame_size(self.notebook_frames)
            self.set_window_size(width=target_width + pad_x, height=target_height + pad_y)
            self.add_status(target_width + pad_x - 5, target_height + pad_y - 8)

        self.update_size = False

    def set_status(self, *xargs, **kwargs):
        """
        The callback function for the status variable.
        This will set the status label and will cause the ellipses to spin
        """
        self.status_value = self.status.get()[:self.status_size]
        self.status_spin = 0

        if self.status_value:
            self.updater(after=False)
        else:
            self.status_label.set('')

    def updater(self, after=True):
        """
        The main updater loop for the gui

        Args:
            after (bool): Flag to indicate whether to schedule another update
        """
        if self.status_value:
            self.status_label.set('(%s%s%s)' % (self.status_value, '.' * self.status_spin, ' ' *
                                                (3 - self.status_spin)))
            self.status_spin = (self.status_spin + 1) % 4

        if after:
            self.root.after(self.update_rate, self.updater)


def set_relative_size(root, minsize=5):
    """
    Set some grid / column sizes

    Args:
        minsize (int): The minimum column and row sizes
    """
    Nc, Nr = root.grid_size()

    for ii in range(Nc):
        root.grid_columnconfigure(ii, minsize=minsize, weight=1)

    for ii in range(Nr):
        root.grid_rowconfigure(ii, minsize=minsize, weight=1)
