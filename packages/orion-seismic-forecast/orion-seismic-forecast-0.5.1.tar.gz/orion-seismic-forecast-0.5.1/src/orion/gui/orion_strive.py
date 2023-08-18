# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
orion_strive.py
--------------------------------------
"""
from strive.dash import dash_gui_base
import orion
import os
from PIL import Image
from dash import html


class OrionSTRIVE(dash_gui_base.DashGUIBase):
    """
    STRIVE-based Orion gui

    Attributes:
        main_buttons (dict): An object to hold the control buttons in the gui
    """

    def __init__(self, **kwargs):
        """
        Main Orion gui initialization
        """
        # Call the parent's initialization
        super().__init__(**kwargs)
        self.banner_subheader = 'Operational Forecasting of Induced Seismicity'

    def get_help_info(self):
        # Help text
        help_text = f'Orion (v{orion.__version__}) with funding support from the United States '
        help_text += 'Department of Energy’s Office of Fossil Energy and Carbon Management through the '
        help_text += 'Science-informed Machine Learning to Accelerate Real-Time (SMART) Decisions in Subsurface '
        help_text += 'Applications Initiative and the National Risk Assessment Partnership (NRAP). '
        help_text += 'The work was funded, in part, through the Bipartisan Infrastructure Law. '
        help_text += 'This support is gratefully acknowledged.'
        help_text += '\n\nThis work was performed under the auspices of the U.S. Department of Energy by Lawrence '
        help_text += 'Livermore National Laboratory under contract DE-AC52-07NA27344, and is '
        help_text += 'released under the identifier LLNL-CODE-842148.'

        # Logos
        gui_source_path = os.path.split(__file__)[0]
        all_logos_path = os.path.join(gui_source_path, 'logos_all.png')
        all_logos_image = Image.open(all_logos_path).resize((638, 432), Image.ANTIALIAS)
        help_div = html.Div(children=[html.P(help_text), html.Img(src=all_logos_image)])

        return help_div


def run(config_fname, profile_run=False):
    """
    Launch the Orion STRIVE gui

    Args:
        config_fname (str): Name of the orion config file
    """

    # Initialize orion
    manager = None
    try:
        from orion.managers import orion_manager
        manager = orion_manager.OrionManager(config_fname=config_fname, skip_data_load=True, frontend='strive')
    except Exception as e:
        print('Failed to load orion')
        print(e)

    # Launch the gui
    if manager:
        title_url = 'https://edx.netl.doe.gov/dataset/orion-operational-forecasting-of-induced-seismicity'
        banner_url_map = {
            'Documentation': {
                'url': 'https://nrap.gitlab.io/orion/'
            },
            'EDX': {
                'url': 'https://edx.netl.doe.gov/workspace/resources/orion'
            }
        }

        gui_source_path = os.path.split(__file__)[0]
        logo_file = os.path.join(gui_source_path, 'orion_logo_simple.png')

        gui = OrionSTRIVE(manager=manager, banner_url=banner_url_map, logo=logo_file, title_url=title_url)
        gui.build_interface()
        gui.run()
