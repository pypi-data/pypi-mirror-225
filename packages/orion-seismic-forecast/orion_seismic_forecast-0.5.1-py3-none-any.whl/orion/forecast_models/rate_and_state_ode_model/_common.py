# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

from numba import jit


def jitted(*args, **kwargs):
    """Custom :func:`jit` with default options."""
    kwargs.update({
        "nopython": True,
        "nogil": True,
    # Disable fast-math flag "nnan" and "reassoc"
    # <https://llvm.org/docs/LangRef.html#fast-math-flags>
        "fastmath": {"ninf", "nsz", "arcp", "contract", "afn"},
    # "boundscheck": False,
        "cache": True,
    })
    return jit(*args, **kwargs)
