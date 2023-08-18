# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import logging
from tkinter import ttk, Canvas, StringVar
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import backend_bases
import numpy as np
import webbrowser


class SilentMatplotlibToolbar(NavigationToolbar2Tk):
    """
    Matplotlib toolbar with cursor status disabled
    """

    def set_message(self, s):
        """
        Disable the cursor status message
        """
        pass


class LabeledScale():
    """
    A ttk scale with labels
    """

    def __init__(self,
                 parent_frame,
                 scale_range=(0.0, 1.0),
                 length=300,
                 Nticks=4,
                 variable=None,
                 command=None,
                 orient='horizontal',
                 label_format='{0:1.1f}'):
        self.frame = ttk.Frame(parent_frame)
        self.label_format = label_format

        # Build tick labels
        self.tick_vals = np.linspace(scale_range[0], scale_range[1], Nticks)
        self.tick_variables = []
        tick_positions = ['center' for x in self.tick_vals]
        tick_positions[0] = 'w'
        tick_positions[-1] = 'e'

        for ii, v in enumerate(self.tick_vals):
            self.tick_variables.append(StringVar())
            self.tick_variables[ii].set(label_format.format(v))
            label = ttk.Label(self.frame, textvariable=self.tick_variables[ii], anchor=tick_positions[ii])
            label.grid(row=0, column=ii, padx=2, sticky='new')

        # Build the scale
        self.scale = ttk.Scale(self.frame,
                               from_=self.tick_vals[0],
                               to=self.tick_vals[-1],
                               length=length,
                               variable=variable,
                               command=command,
                               orient=orient)
        self.scale.grid(row=1, column=0, columnspan=Nticks, padx=2, sticky='sew')

    def configure(self, *xargs, **kwargs):
        if ('label_format' in kwargs):
            self.label_format = kwargs['label_format']
        if ('scale_range' in kwargs):
            Nticks = len(self.tick_vals)
            self.tick_vals = np.linspace(kwargs['scale_range'][0], kwargs['scale_range'][1], Nticks)
            for ii, v in enumerate(self.tick_vals):
                self.tick_variables[ii].set(self.label_format.format(v))

            self.scale.configure(from_=self.tick_vals[0], to=self.tick_vals[-1])

    def grid(self, *xargs, **kwargs):
        self.frame.grid(*xargs, **kwargs)


class CompactNotebook(ttk.Notebook):
    """
    Notebook that compresses the number of tabs visible at any given time

    Attributes:
        max_short_len (int): Max length of the tab name when not highlighted
        max_long_len (int): Max length of the tab name when highlighted
        short_names (list): List of tab names to show when not highlighted
        long_names (list): List of tab names to show when highlighted
        N (int): The number of tabs
        max_tabs (int): The max number of tabs to show at any time
        active_tabs (list): The index of active tabs
        left_button (ttk.Frame): Left button handle
        right_button (ttk.Frame): Right button handle
    """

    def __init__(self, parent, max_tabs=8):
        super().__init__(parent)

        # Name config
        self.max_short_len = 20
        self.max_long_len = 30
        self.short_names = []
        self.long_names = []

        # Tab placeholders
        self.N = 0
        self.max_tabs = max_tabs
        self.active_tabs = []
        self.hidden_tabs = {}
        self.last_visibility = {}

        # Navigation buttons
        self.left_button = ttk.Frame(parent)
        self.right_button = ttk.Frame(parent)
        super().add(self.left_button, text='<')
        super().add(self.right_button, text='>')
        self.hide_left_button()
        self.hide_right_button()

        # Events
        self.bind('<<NotebookTabChanged>>', self.udpate_tab_visibility)

    def add(self, child, **kwargs):
        """
        Add a tab to the notebook

        Args:
            child (ttk.Frame): The frame to add to the notebook
        """
        self.N += 1
        super().insert(self.N, child, **kwargs)
        self.active_tabs.append(self.N)
        self.select(self.N)

        name = 'tab_name'
        if ('text' in kwargs):
            name = kwargs['text']
        M = len(name)
        self.short_names.append(name[:min(M, self.max_short_len)])
        self.long_names.append(name[:min(M, self.max_long_len)])

        self.udpate_tab_visibility()

    def forget(self, tab_id):
        """
        Remove a tab from the notebook

        Args:
            tab_id (int): The index of the tab to be deleted
        """
        # Check to see if the tab is being rendered
        self.N -= 1
        tab_index = 0
        try:
            tab_index = self.index(tab_id)
        except Exception as e:
            print(e)
            return

        if tab_index in self.active_tabs:
            self.active_tabs.remove(tab_index)
        for ii in range(len(self.active_tabs)):
            if (self.active_tabs[ii] > tab_index):
                self.active_tabs[ii] -= 1

        # Remove the tab
        super().forget(tab_id)
        if len(self.active_tabs):
            self.select(self.active_tabs[-1])
        del self.short_names[tab_index - 1]
        del self.long_names[tab_index - 1]
        self.udpate_tab_visibility()

    def get_current_tab_name(self):
        """
        Get the current tab name

        Returns:
            str: The current long-tab name
        """
        if len(self.active_tabs):
            current_index = self.index(self.select())
            return self.long_names[current_index - 1]
        else:
            return "None"

    def show_left_button(self):
        """
        Add the left button to the notebook
        """
        super().add(self.left_button)

    def hide_left_button(self):
        """
        Remove the left button from the notebook
        """
        self.hide(0)

    def show_right_button(self):
        """
        Add the right button to the notebook
        """
        super().add(self.right_button)

    def hide_right_button(self):
        """
        Remove the right button from the notebook
        """
        self.hide(self.N + 1)

    def compressed_view(self):
        # Update button visibility
        if (self.active_tabs[0] == 1):
            self.hide_left_button()
        else:
            self.show_left_button()

        if (self.active_tabs[-1] == self.N):
            self.hide_right_button()
        else:
            self.show_right_button()

        # Update tab visibility
        M = len(self.active_tabs)
        if (M > self.max_tabs):
            # Check for newly added tabs, moving the window to the right
            new_active_tabs = list(range(self.N - self.max_tabs + 1, self.N + 1))
            for ii in self.active_tabs:
                if ii not in new_active_tabs:
                    self.hide(ii)
            for ii in new_active_tabs:
                if ii not in self.active_tabs:
                    super().add(self.tabs()[ii])
            self.active_tabs = new_active_tabs

        elif (M < self.max_tabs):
            # Check for newly removed tabs, moving the window appropriately
            new_active_tabs = []
            if (self.active_tabs[-1] < self.N):
                # Prefer tabs to the right
                tabs_to_right = self.N - self.active_tabs[-1]
                tabs_to_add = max(tabs_to_right, self.max_tabs - M)
                new_active_tabs = list(range(self.active_tabs[-1] + 1, self.active_tabs[-1] + 1 + tabs_to_add))

            if (len(new_active_tabs) + M < self.max_tabs):
                tabs_to_left = self.active_tabs[0] - 1
                tabs_to_add = max(tabs_to_left, self.max_tabs - M - len(new_active_tabs) - 1)
                tmp = list(range(self.active_tabs[0] - tabs_to_add, self.active_tabs[0]))
                new_active_tabs.extend(tmp)

            for ii in new_active_tabs:
                super().add(self.tabs()[ii])
            self.active_tabs.extend(new_active_tabs)

        # Button presses
        current_index = self.index(self.select())
        new_active_tabs = []
        if (current_index == 0):
            start_index = max(self.active_tabs[0] - self.max_tabs, 1)
            new_active_tabs = list(range(start_index, start_index + self.max_tabs))
            self.select(self.active_tabs[-1])
        if (current_index > self.N):
            end_index = min(self.active_tabs[-1] + self.max_tabs, self.N)
            new_active_tabs = list(range(end_index - self.max_tabs + 1, end_index + 1))
            self.select(self.active_tabs[-1])

        if len(new_active_tabs):
            for ii in self.active_tabs:
                if ii not in new_active_tabs:
                    self.hide(ii)
            for ii in new_active_tabs:
                if ii not in self.active_tabs:
                    super().add(self.tabs()[ii])
            self.active_tabs = new_active_tabs
            self.select(self.active_tabs[-1])

    def expanded_view(self):
        self.hide_left_button()
        self.hide_right_button()

        if (len(self.active_tabs) != self.N):
            # Make sure all of the tabs are shown
            for ii in range(1, self.N + 1):
                if ii not in self.active_tabs:
                    super().add(self.tabs()[ii])

    def select_first_tab(self):
        """
        Select the first tab
        """
        try:
            # N = max(len(self.active_tabs), self.max_tabs)
            if len(self.active_tabs) > 1:
                N = min(len(self.active_tabs), self.max_tabs)
                self.active_tabs = list(range(1, N + 1))
                self.select(1)
                self.udpate_tab_visibility()
        except Exception as e:
            # print(e)
            pass

    def set_tab_visibility(self, visiblity):
        """
        Set the manual visibility flag for tabs in the notebook
        """
        for k, v in visiblity.items():
            if v:
                if k not in self.long_names:
                    # Add a tab back into the notebook
                    if k in self.hidden_tabs:
                        x = self.hidden_tabs.pop(k)
                        self.add(x, text=k)
            elif k in self.long_names:
                ii = self.long_names.index(k) + 1
                self.hidden_tabs[k] = self.tabs()[ii]
                self.forget(ii)

    def udpate_tab_visibility(self, *args):
        """
        Update the active tab visibility, and hide/show the
        left/right buttons as necessary
        """
        if (self.N > self.max_tabs):
            self.compressed_view()
        else:
            self.expanded_view()

        # Update tab labels
        self.active_tabs = sorted(self.active_tabs)
        if (self.N > 0):
            current_index = self.index(self.select())
            for ii in self.active_tabs:
                if (ii == current_index):
                    self.tab(ii, text=self.long_names[ii - 1])
                else:
                    self.tab(ii, text=self.short_names[ii - 1])


class AutoScrollbar(ttk.Scrollbar):

    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        super().set(low, high)


class ScrollableFrame(ttk.Frame):
    """
    A modified ttk frame that is scrollable when either or both
    axes are smaller than their contents

    Attributes:
        canvas (tkinter.Canvas): The canvas that holds the child frame
        scrollbar_x (AutoScrollbar): The scrollbar for the x-axis
        scrollbar_y (AutoScrollbar): The scrollbar for the y-axis
        scrollable_frame (ttk.Frame): The frame that holds the child objects
    """

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        self.scrollbar_x = AutoScrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_y = AutoScrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

        self.canvas.grid(column=0, row=0, sticky='news', padx=1, pady=1)
        self.scrollbar_y.grid(column=1, row=0, sticky='ns')
        self.scrollbar_x.grid(column=0, row=1, sticky='ew')
        self.grid_columnconfigure(0, minsize=10, weight=1)
        self.grid_rowconfigure(0, minsize=10, weight=1)

        self.scrollable_frame.bind("<Configure>", self.size_updater)

    def size_updater(self, *args, **kwargs):
        """
        Callback function that maintains the proper frame size
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def open_link_factory(url):
    """
    Small factory to open links in the user's default browser
    """

    def open_link(*xargs, **kwargs):
        webbrowser.open(url)

    return open_link


class ListHandler(logging.Handler):
    """
    Class to record logging messages in a list
    """

    def __init__(self, log_list):
        logging.Handler.__init__(self)
        self.log_list = log_list

    def emit(self, record):
        self.log_list.append(record.msg)


# Setup matplotlib navigation toolbars
backend_bases.NavigationToolbar2.toolitems = (
    ('Home', None, 'home', 'home'),
    (None, None, None, None),
    (None, None, None, None),
    ('Pan', None, 'move', 'pan'),
    ('Zoom', None, 'zoom_to_rect', 'zoom'),
    (None, None, None, None),
    ('Save', None, 'filesave', 'save_figure'),
)
