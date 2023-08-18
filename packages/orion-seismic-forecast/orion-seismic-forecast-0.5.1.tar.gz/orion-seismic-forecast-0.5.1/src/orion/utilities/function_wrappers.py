# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
function_wrappers.py
-----------------------
"""

import numpy as np


class constant_fn():
    """
    Factory to return a constant function with N arguments

    Args:
        value (float): A constant value

    Returns:
        function: A constant value function
    """

    def __init__(self, value):
        self.value = value

    def __call__(self, *args):
        result = 0.0
        if isinstance(args[0], np.ndarray):
            result = np.zeros(np.shape(args[0])) + self.value
        else:
            result += self.value
        return result


class variable_len_fn():
    """
    Factory to handle mismatches between the number of
    inputs to the original function.  If the number of
    arguments in greater than the original, the additional
    values will be ignored.  If the number of arguments
    is smaller than the original, they will be padded with zeros

    Args:
        original_fn (scipy.interpolate.LinearNDInterpolator): The original interpolation function
        Ndim (int): The expected number of arguments to the original function
        list_arg (bool): Flag to indicate whether arguments to the function should be converted to a list (default=False)

    Returns:
        function: The wrapped function
    """

    def __init__(self, original_fn, Ndim, list_arg=False):
        self.original_fn = original_fn
        self.Ndim = Ndim
        self.list_arg = list_arg

    def __call__(self, *args):
        # Handle the argument length
        Nargs = len(args)
        if (Nargs < self.Ndim):
            args.extend([0.0 for x in range(self.Ndim - Nargs)])
        elif (Nargs > self.Ndim):
            args = args[:self.Ndim]

        # Handle the argument type
        result = 0.0
        if self.list_arg:
            result = self.original_fn(args)
        else:
            result = self.original_fn(*args)
        return result


class masked_fn():
    """
    Factory to ignore unnecessary positional arguments to a function

    Args:
        original_fn (scipy.interpolate.LinearNDInterpolator): The original interpolation function
        mask (list): list of bools indicating which arguments to keep
        list_arg (bool): Flag to indicate whether arguments to the function should be converted to a list (default=False)

    Returns:
        function: The wrapped function
    """

    def __init__(self, original_fn, mask, list_arg=False):
        self.original_fn = original_fn
        self.mask = mask
        self.list_arg = list_arg

    def __call__(self, *args):
        # Handle the argument length
        new_args = tuple([args[ii] for ii in self.mask])
        if self.list_arg:
            return self.original_fn(new_args)
        else:
            return self.original_fn(*new_args)
