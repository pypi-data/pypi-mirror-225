# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
about_gui.py
--------------------------------------
"""

import os
from tkinter import ttk
import orion
from orion.gui.gui_base import GUIBase, set_relative_size
from orion.utilities.plot_config import gui_colors
from orion.gui.custom_widgets import open_link_factory
from PIL import Image, ImageTk


class AboutGUI(GUIBase):
    """
    Orion information gui
    """

    def __init__(self, parent):
        """
        Orion information gui initialization
        """
        # Call the parent's initialization
        super().__init__(parent.child_gui['about']['window'])

        # Gui-specific parameters
        self.parent = parent

        self.about_string = f'Orion (v{orion.__version__}) with funding support from the United States '
        self.about_string += 'Department of Energy’s Office of Fossil Energy and Carbon Management through the '
        self.about_string += 'Science-informed Machine Learning to Accelerate Real-Time (SMART) Decisions in Subsurface '
        self.about_string += 'Applications Initiative and the National Risk Assessment Partnership (NRAP). '
        self.about_string += 'The work was funded, in part, through the Bipartisan Infrastructure Law. '
        self.about_string += 'This support is gratefully acknowledged.'
        self.about_string += '\n\nThis work was performed under the auspices of the U.S. Department of Energy by Lawrence '
        self.about_string += 'Livermore National Laboratory under contract DE-AC52-07NA27344, and is '
        self.about_string += 'released under the identifier LLNL-CODE-842148.'

        # Logos (1276x863)
        all_logos_path = os.path.join(self.gui_source_path, 'logos_all.png')
        self.all_logos_image = Image.open(all_logos_path).resize((638, 432), Image.ANTIALIAS)
        self.all_logos = ImageTk.PhotoImage(self.all_logos_image)

        self.create_main()
        self.set_icon()

    def quit(self):
        """
        Close the config gui
        """
        self.window.withdraw()
        self.window.destroy()
        del self.parent.child_gui['about']

    def create_main(self):
        """
        Create the config gui main page
        """
        # Create the main window
        self.frame.pack(fill='both', expand=True)
        self.window.title("About Orion")
        self.window.protocol('WM_DELETE_WINDOW', self.quit)

        # Add text
        about_text_label = ttk.Label(self.frame, text=self.about_string, wraplength=700)
        about_text_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='new')

        # Links
        documentation_label = ttk.Label(self.frame,
                                        text='Documentation',
                                        foreground=gui_colors.theme['blue'],
                                        cursor="hand2")
        documentation_label.grid(row=1, column=0, padx=5, pady=5, sticky='new')
        documentation_label.bind("<Button-1>", open_link_factory(orion.documentation_url))

        license_label = ttk.Label(self.frame,
                                  text='License Information',
                                  foreground=gui_colors.theme['blue'],
                                  cursor="hand2")
        license_label.grid(row=1, column=1, padx=5, pady=5, sticky='new')
        license_label.bind("<Button-1>", open_link_factory(orion.license_url))

        smart_label = ttk.Label(self.frame, text='SMART', foreground=gui_colors.theme['blue'], cursor="hand2")
        smart_label.grid(row=2, column=0, padx=5, pady=5, sticky='new')
        smart_label.bind("<Button-1>", open_link_factory(orion.smart_url))

        nrap_label = ttk.Label(self.frame, text='NRAP', foreground=gui_colors.theme['blue'], cursor="hand2")
        nrap_label.grid(row=2, column=1, padx=5, pady=5, sticky='new')
        nrap_label.bind("<Button-1>", open_link_factory(orion.nrap_url))

        edx_label = ttk.Label(self.frame, text='Orion EDX', foreground=gui_colors.theme['blue'], cursor="hand2")
        edx_label.grid(row=2, column=2, padx=5, pady=5, sticky='new')
        edx_label.bind("<Button-1>", open_link_factory(orion.edx_url))

        # Add logos
        all_logos_label = ttk.Label(self.frame, image=self.all_logos)
        all_logos_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='ews')

        set_relative_size(self.frame)
