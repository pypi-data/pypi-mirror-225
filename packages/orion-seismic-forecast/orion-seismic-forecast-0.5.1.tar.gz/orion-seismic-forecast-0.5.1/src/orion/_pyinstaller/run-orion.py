# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""Entry point for pyinstaller"""

import multiprocessing
import sys
import time


def main():
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    try:
        import pyi_splash
        pyi_splash.update_text("Loading Orion...")
        # print('Starting orion')
        from orion.gui import orion_gui
        pyi_splash.close()
        orion_gui.launch_gui('')
    except Exception as e:
        print(e)
    except:
        # print('Orion did not launch...')
        pass

    # print(' ', flush=True)
    # while True:
    #     time.sleep(1)


if __name__ == "__main__":
    main()
