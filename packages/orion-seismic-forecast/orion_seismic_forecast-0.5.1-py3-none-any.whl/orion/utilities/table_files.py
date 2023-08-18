# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
table_files.py
-----------------------
"""

import os
import numpy as np
import logging
from scipy.interpolate import LinearNDInterpolator, RegularGridInterpolator, interp1d
from orion.utilities import function_wrappers, hdf5_wrapper, file_io

logger = logging.getLogger('orion_logger')


def load_table_files(data, axes_names=['x', 'y', 'z', 't']):
    """
    Load structured or unstructured property values

    Attributes:
        data: Dictionary of table entries
        axes_names: List of potential axes names
    """
    logger.debug('Checking table file shape')
    file_io.check_table_shape(data)
    table_interpolators = {}
    pnames = [k for k in data.keys() if k not in axes_names]

    # Check to see which axes are present
    active_axes = [k for k in axes_names if k in data.keys()]
    function_mask = [ii for ii, k in enumerate(axes_names) if k in active_axes]

    # Check to see if the data is structured/unstructured
    if (len(np.shape(data[pnames[0]])) > 1):
        logger.debug('Table files appear to be structured')

        # The data appears to be structured
        points = []
        for k in active_axes:
            points.append(data[k])

        for p in pnames:
            logger.debug(f'Generating grid interpolator: {p}')
            tmp = RegularGridInterpolator(tuple(points),
                                          np.ascontiguousarray(data[p]),
                                          bounds_error=False,
                                          fill_value=None)
            table_interpolators[p] = function_wrappers.masked_fn(tmp, function_mask, list_arg=True)

    else:
        # Unstructured data
        logger.debug('Table files appear to be unstructured')
        points = []
        for k in active_axes:
            points.append(np.reshape(data[k], (-1, 1)))

        tmp = np.meshgrid(*points, indexing='ij')
        points = [np.reshape(x, (-1, 1), order='F') for x in tmp]
        points = np.ascontiguousarray(np.squeeze(np.concatenate(points, axis=1)))

        # Load the data
        for p in pnames:
            if (points.ndim == 1):
                logger.debug(f'Generating 1D interpolator: {p}')
                pval = np.squeeze(data[p])
                tmp = interp1d(points, pval, kind='linear', bounds_error=False, fill_value=(pval[0], pval[-1]))
                table_interpolators[p] = function_wrappers.masked_fn(tmp, function_mask)
            else:
                logger.debug(f'Generating ND interpolator: {p}')
                pval = np.reshape(data[p], (-1, 1), order='F')
                tmp = LinearNDInterpolator(points, pval, fill_value=0.0)
                table_interpolators[p] = function_wrappers.masked_fn(tmp, function_mask)

    return table_interpolators


def save_table_files(fname, data, axes_names=['x', 'y', 'z', 't']):
    fname = os.path.expanduser(fname)

    if ('hdf5' in fname):
        root_dir = os.path.dirname(fname)
        if root_dir:
            os.makedirs(root_dir, exist_ok=True)
        with hdf5_wrapper.hdf5_wrapper(fname, mode='w') as f:
            for k, v in data.items():
                f[k] = np.ascontiguousarray(v)
    elif ('.' not in fname):
        os.makedirs(fname, exist_ok=True)
        for k in axes_names:
            np.savetxt(os.path.join(fname, f'{k}.csv'), np.squeeze(data[k]), delimiter=',')
        for k in data.keys():
            if k not in axes_names:
                tmp = np.reshape(np.ascontiguousarray(data[k]), (-1), order='f')
                np.savetxt(os.path.join(fname, f'{k}.csv'), tmp, delimiter=',')

    else:
        logger.warning('Table files can be saved to an .hdf5 format file or a folder (containing .csv)')
