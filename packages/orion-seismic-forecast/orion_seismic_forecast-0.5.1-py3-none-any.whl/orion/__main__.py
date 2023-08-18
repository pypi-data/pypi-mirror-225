# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""Command line tools for orion"""

import argparse
import os


def main():
    """
    Entry point for Orion

    Args:
        -c/--config Optional config filename
        -n/--no_gui Optional flag to disable gui (default=0)
    """

    # Parse the user arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help='Orion json config file', default='')
    parser.add_argument('-i', '--ignore_cache', action='store_true', help='Ignore the cache file when running')
    parser.add_argument('-f', '--frontend', type=str, help='GUI frontend (tkinter, strive, or none)', default='tkinter')
    parser.add_argument('-s', '--schema', type=str, help='Generate the schema', default='')
    args = parser.parse_args()

    if args.schema:
        from orion.gui import gui_api
        gui_api.write_schema(args.schema)
        return

    if args.ignore_cache:
        cache_root = os.path.expanduser('~/.cache/orion')
        cache_file = os.path.join(cache_root, 'orion_config.json')
        if os.path.isfile(cache_file):
            print('Ignoring cached values')
            os.remove(cache_file)

    import orion
    if args.frontend == 'tkinter':
        orion._frontend = 'tkinter'
        from orion.gui import orion_gui
        orion_gui.launch_gui(args.config)
    elif args.frontend == 'strive':
        orion._frontend = 'strive'
        from orion.gui import orion_strive
        orion_strive.run(args.config)
    else:
        orion._frontend = ''
        from orion.managers import orion_manager
        orion_manager.run_manager(args.config)


if __name__ == "__main__":
    main()
