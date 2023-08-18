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
from tkinter import filedialog
import utm    # type: ignore[import]
import urllib
import os
import tempfile
import glob
import datetime
import logging

logger = logging.getLogger('orion_logger')


def load_CA_DOGGR_OilGas_data(epoch_start, epoch_stop):
    """
    Loads well data from California DOGGR Oil/Gas site

    Args:
        epoch_start (int): Data request start time (seconds, epoch)
        epoch_stop (int): Data request stop time (seconds, epoch)

    Returns:
        dict: segment_data (or list of dicts)
    """
    logger.warning('CA_DOGGR_OilGas data not supported yet')
    segment_data = {}
    return segment_data


def load_CA_DOGGR_Geothermal_data(epoch_start, epoch_stop):
    """
    Loads well data from California DOGGR Geothermal site

    Args:
        epoch_start (int): Data request start time (seconds, epoch)
        epoch_stop (int): Data request stop time (seconds, epoch)

    Returns:
        dict: segment_data (or list of dicts)
    """
    logger.info('Attempting to download data from CA GeoSteam')
    data, metadata = fetch_geosteam_data()

    # Process the data so that they are on the same vector
    epoch_common = np.unique(np.concatenate([data[k]['epoch'] for k in data.keys()], axis=0))
    N = len(epoch_common)
    segment_range = epoch_common[[0, -1]]
    uniform_data = {}
    for ka in data.keys():
        uniform_data[ka] = {}
        isect = np.intersect1d(data[ka]['epoch'], epoch_common, return_indices=True)
        for kb in data[ka].keys():
            if (kb != 'epoch'):
                tmp_val = np.zeros(N)
                tmp_val[isect[2]] = data[ka][kb][isect[1]]
                uniform_data[ka][kb] = tmp_val

    # Assemble the segment
    segment = {'segment_range': segment_range, 'epoch': epoch_common, 'data': uniform_data, 'metadata': metadata}

    return segment


def fetch_geosteam_data(well_summary_fname=''):
    """
    Fetch well data from California GeoSteam site

    Args:
        well_summary_fname (str): Path to GeoSteam well summary file (.xlsx)

    Returns:
        dict: dictionary of well data
    """
    import pandas as pd
    request_format = 'https://geosteam.conservation.ca.gov/GeoWellSearch/ExportToExcel%sReport?apinum=%08d'
    request_types = ['Injection', 'Steam']

    # Select well file
    if not well_summary_fname:
        logger.info('Select a CA GeoSteam summary file to download well data')
        logger.info('These can be found at the following URL:')
        logger.info('https://geosteam.conservation.ca.gov/GeoWellSearch')
        well_summary_fname = filedialog.askopenfilename(title='Select a CA GeoSteam summary file (xlsx)',
                                                        filetypes=(("xlsx", "*.xlsx"), ("all", "*.*")))
    wells = pd.read_excel(well_summary_fname)
    api_numbers = wells['API'].to_numpy(copy=True, dtype=int)
    latitude = wells['(HUD) Latitude'].to_numpy(copy=True, dtype=float)
    longitude = wells['Longitude'].to_numpy(copy=True, dtype=float)

    # For wells with missing lat/lon, place them in the middle of the request
    latitude[np.isnan(latitude)] = np.nanmean(latitude)
    longitude[np.isnan(longitude)] = np.nanmean(longitude)

    # Convert locations to UTM
    tmp_utm = utm.from_latlon(latitude, longitude)
    easting = tmp_utm[0]
    northing = tmp_utm[1]
    catalog_utm_zone = str(tmp_utm[2]) + tmp_utm[3]

    # Fetch data
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    logger.debug(f'Download directory: {tmp_path}')
    for ii in api_numbers:
        logger.info(f'Fetching data for well {ii}')
        for r in request_types:
            logger.info(f'  {r}')
            url = request_format.format(r, ii)
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urllib.request.urlopen(req).read()
                with open(os.path.join(tmp_path, f'{r}_{ii:08d}.xlsx'), 'wb') as f:
                    f.write(webpage)
            except:
                logger.error(f'    (data not available for well: {ii})')

    # Parse data
    well_data = {}
    well_metadata = {}
    well_types = [['Injection', 'Water Injection Rate (1000 kg/hr)', 1.0 / 3600.0],
                  ['Steam', 'Steam Prod Rate (1000 kg/hr)', -1.0 / 3600.0]]

    for wd in well_types:
        for f in glob.glob(os.path.join(tmp_path, f'{wd[0]}_*.xlsx')):
            df = pd.read_excel(f)
            if df.empty:
                continue

            w = parse_geosteam_well_data(df,
                                         well_type=wd[0],
                                         targets={
                                             'pressure': ['Pressure (bars)', 1e5],
                                             'flow_rate': wd[1:],
                                             'temperature': ['Temperature (C)', 1.0]
                                         })
            for k, v in w.items():
                well_data[k] = v

            well_metadata[k] = {}
            tmp_doi = int(k.split('_')[1])
            Ia = np.where(api_numbers == tmp_doi)[0][0]
            well_metadata[k]['latitude'] = latitude[Ia]
            well_metadata[k]['longitude'] = longitude[Ia]
            well_metadata[k]['easting'] = easting[Ia]
            well_metadata[k]['northing'] = northing[Ia]
            well_metadata[k]['depth'] = 0.0
            well_metadata[k]['utm_zone'] = catalog_utm_zone
            well_metadata[k]['api'] = tmp_doi

    return well_data, well_metadata


def parse_geosteam_well_data(well_df, well_type='injection', targets={}):
    """
    Fetch well data from California GeoSteam site

    Args:
        well_df (pandas.data_frame): Data frame for GeoSteam well file
        well_type (str): Header to use for well name
        targets (dict): Dictionary of parameter names pointing to lists of excel names, scale factors

    Returns:
        dict: dictionary of well data
    """
    # Parse well name
    well_df = well_df.drop(well_df[well_df['API Number'] == 'TOTAL'].index)
    well_name = f'{well_type}_{well_df["API Number"][0]}'

    # Convert timestamps
    t_month = well_df['Month'].to_numpy(dtype=int, copy=True)
    t_year = well_df['Year'].to_numpy(dtype=int, copy=True)
    N = len(t_month)
    epoch = np.zeros(N, dtype=int)
    for ii in range(N):
        ts = datetime.datetime(t_year[ii], t_month[ii], 1)
        epoch[ii] = ts.timestamp()

    Ia = np.argsort(epoch)
    data = {well_name: {'epoch': epoch[Ia]}}
    for k in targets.keys():
        data[well_name][k] = well_df[targets[k][0]].to_numpy(dtype=float, copy=True)[Ia] * targets[k][1]

    return data
