# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
file_io.py
-----------------------
"""

import numpy as np
from orion.utilities import unit_conversion
import requests
import urllib3
import warnings
from contextlib import contextmanager

# Note: The existing code tends to use pandas to read from csv files.
#       We may want to consider switching to the native numpy reader if
#       if we don't need to leverage more of the package, since it is heavy-weight.
#       We could also consider relying on hfd5-format files for IO, especially if
#       we are expecting to handle large files.

# TODO: Move file reading utilities here
# TODO: Consider changing all timestamps to the unix epoch, rather than moving around datestrings


# Old Methods
def read_zmap_catalog(filename):
    """
    function description

    @arg filename filename
    """
    names = ['lat', 'lon', 'dec_year', 'month', 'day', 'mag', 'depth', 'hour', 'minute', 'second']
    df_cat = pd.read_csv(filename, sep='\s+', names=names)
    df_cat['year'] = np.floor(df_cat.dec_year)
    df_temp = df_cat[['year', 'month', 'day', 'hour', 'minute', 'second']]
    df_cat['date'] = pd.to_datetime(df_temp)
    df_cat = df_cat.drop(columns=['dec_year', 'year', 'month', 'day', 'hour', 'minute', 'second'])
    return df_cat


def read_flowfile(filename):
    """
    read flowfile with year month day hour minute second flow pressure constant

    @arg filename filename
    """
    names = ['year', 'month', 'day', 'hour', 'minute', 'second', 'flow', 'pressure', 'const']
    df_fr = pd.read_csv(filename, sep='\s+', names=names)
    df_temp = df_fr[['year', 'month', 'day', 'hour', 'minute', 'second']]
    df_fr['date'] = pd.to_datetime(df_temp)
    df_fr = df_fr.drop(columns=['year', 'month', 'day', 'hour', 'minute', 'second'])
    df_fr['flow'] = df_fr['flow'] / 1e3    # convert from liter/min to m3  pl
    # convert from liter/min to m3
    df_fr['dt'] = df_fr['date'].diff() / np.timedelta64(1, 'm')
    df_fr['fluid_volume'] = df_fr['flow'] * df_fr['dt']
    df_fr['fluid_volume_cumulative'] = np.cumsum(df_fr['fluid_volume'])
    df_fr = df_fr.drop(columns=['dt', 'fluid_volume'])
    return df_fr


def parse_csv(fname):
    """
    Parse csv file with headers, units

    Args:
            fname (string): Filename
            header_size (int): number of header lines

    Returns:
            dict: File results

    """
    # Check headers
    headers = []
    header_size = 0
    units_scale = []
    with open(fname) as f:
        headers = [x.strip() for x in f.readline()[1:-1].split(',')]
        tmp = f.readline()
        if ('#' in tmp):
            header_size += 1
            unit_converter = unit_conversion.UnitManager()
            units = [x.strip() for x in tmp[1:].split(',')]
            units_scale = [unit_converter(x) for x in units]
        else:
            units_scale = np.ones(len(headers))

    # Parse body
    tmp = np.loadtxt(fname, unpack=True, delimiter=',', skiprows=header_size)
    data = {headers[ii]: tmp[ii] * units_scale[ii] for ii in range(len(headers))}

    return data


def check_table_shape(data, axes_names=['x', 'y', 'z', 't']):
    """
    Check shape of table arrays

    Attributes:
        data: Dictionary of table entries
        axes_names: List of potential axes names
    """
    pnames = [k for k in data.keys() if k not in axes_names]

    # Check to see if the data needs to be reshaped
    structured_shape = tuple([len(data[k]) for k in axes_names if k in data])
    for k in pnames:
        data[k] = np.reshape(data[k], structured_shape, order='F')


@contextmanager
def disable_ssl_warnings():
    """
    Disable ssl warnings in the attached context
    """
    with warnings.catch_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        yield None


def patch_request_get():
    """
    Patch the requests.get method to allow for self-signed certificates,
    which are common on many corporate networks.
    """
    if not hasattr(requests, 'original_get_fn'):
        requests.original_get_fn = requests.get

        def get_allow_self_signed_certs(*xargs, **kwargs):
            """
            If needed, add verify=False to the get arguments
            """
            try:
                return requests.original_get_fn(*xargs, **kwargs)
            except requests.exceptions.SSLError:
                with disable_ssl_warnings():
                    if 'verify' not in kwargs:
                        kwargs['verify'] = False
                    return requests.original_get_fn(*xargs, **kwargs)

        requests.get = get_allow_self_signed_certs
