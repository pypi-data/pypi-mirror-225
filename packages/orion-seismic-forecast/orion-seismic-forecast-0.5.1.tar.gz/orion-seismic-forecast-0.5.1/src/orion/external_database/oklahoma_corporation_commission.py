# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
ca_geosteam.py
-----------------------
"""
import numpy as np
import utm
import urllib
import os
import tempfile
import time
import datetime
import logging
import re
import calendar

logger = logging.getLogger('orion_logger')


def load_OK_Corp_Commission_data(epoch_start, epoch_stop):
    """
    Loads well data from Oklahoma Corporation Commission site

    Args:
        epoch_start (int): Data request start time (seconds, epoch)
        epoch_stop (int): Data request stop time (seconds, epoch)

    Returns:
        dict: segment_data (or list of dicts)
    """
    # Config
    # TODO: Update these by loading the target site
    import pandas as pd
    yearly_catalog_range = [2011, 2022]
    yearly_url = f'https://oklahoma.gov/content/dam/ok/en/occ/documents/og/ogdatafiles/{{}}-uic-injection-volumes.xlsx'

    # Parse requests
    logger.debug('Parsing data request')
    begin_year = max(time.gmtime(epoch_start).tm_year, yearly_catalog_range[0])
    end_year = min(time.gmtime(epoch_stop).tm_year, yearly_catalog_range[1])
    if (begin_year > end_year):
        logger.warning('OK_Corp_Commission data request range not available')
        return []

    # Download well data to a temporary directory for processing
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    tmp_files = []
    tmp_data_ranges = []
    logger.debug(f'Downloading data to a temporary location ({tmp_path})')
    for ii in range(begin_year, end_year + 1):
        url = ''
        ta = datetime.datetime(ii, 1, 1).timestamp()
        tb = min(datetime.datetime(ii + 1, 1, 1).timestamp(), time.time())
        tmp_data_ranges.append([int(ta), int(tb)])
        url = yearly_url.format(ii)

        target_name = f'ok_well_data_{ii}.xlsx'
        logger.info(f'Downloading well data: {target_name}')
        tmp_files.append(os.path.join(tmp_path, target_name))
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request) as response:
            binary_xlsx = response.read()
            with open(tmp_files[-1], 'wb') as f:
                f.write(binary_xlsx)

    # Parse well data
    logger.debug('Parsing well data')
    new_data = []
    for fname, tr in zip(tmp_files, tmp_data_ranges):
        f = pd.read_excel(fname)
        lat = f['LAT'].to_numpy()
        lon = f['LON'].to_numpy()
        depth = f['TotalDepth'].to_numpy()
        well_id = f['API'].to_numpy()
        file_year = f['ReportYear'][0].year
        valid_data = ~(np.isnan(lat) | np.isnan(lon))

        # Cleanup well names
        well_number_raw = f['WellNumber'].to_numpy(dtype=str)
        well_name_raw = f['WellName'].to_numpy(dtype=str)
        sanitize_pattern = re.compile(r'[^\w]')
        well_name = [sanitize_pattern.sub('', f'{ka}_{kb}').strip() for ka, kb in zip(well_name_raw, well_number_raw)]

        # Convert units
        t = [datetime.datetime(file_year, ii + 1, 1).timestamp() for ii in range(12)]
        dt = np.diff(np.concatenate([t, [datetime.datetime(file_year + 1, 1, 1).timestamp()]], axis=0))
        v = np.array([f[f'{m} Vol'].to_numpy() for m in calendar.month_abbr[1:]], dtype=float)
        q = v / np.expand_dims(dt, -1)
        p = np.array([f[f'{m} PSI'].to_numpy() for m in calendar.month_abbr[1:]], dtype=float)
        p *= 6894.76

        # Format data
        logger.debug(f'Constructing data segment for file: {fname}')
        segment = {'segment_range': tr, 'epoch': t, 'data': {}, 'metadata': {}}
        for ii, w in enumerate(well_name):
            if valid_data[ii]:
                well_utm = utm.from_latlon(lat[ii], lon[ii])
                segment['metadata'][w] = {
                    'latitude': lat[ii],
                    'longitude': lon[ii],
                    'depth': depth[ii],
                    'api': well_id[ii],
                    'easting': well_utm[0],
                    'northing': well_utm[1],
                    'utm_zone': str(well_utm[2]) + well_utm[3]
                }
                segment['data'][w] = {'pressure': p[:, ii], 'flow_rate': q[:, ii]}
        new_data.append(segment)

    return new_data
