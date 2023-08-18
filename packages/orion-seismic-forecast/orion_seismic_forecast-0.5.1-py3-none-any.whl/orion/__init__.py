# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

from .__about__ import __version__
from importlib.util import find_spec
from pathlib import Path

# Key url's
documentation_url = 'https://nrap.gitlab.io/orion/'
license_url = 'https://gitlab.com/NRAP/orion/-/blob/develop/LICENSE'
smart_url = 'https://edx.netl.doe.gov/smart/'
nrap_url = 'https://edx.netl.doe.gov/nrap/'
edx_url = 'https://edx.netl.doe.gov/workspace/resources/orion'

# Check for optional packages
optional_packages = []

for k in ['tensorflow', 'csep']:
    if find_spec(k):
        optional_packages.append(k)

# Frontend
_frontend = 'strive'


# Tell PyInstaller where to find hook-orion.py
def _pyinstaller_hooks_dir():
    return [str(Path(__file__).with_name("_pyinstaller").resolve())]
