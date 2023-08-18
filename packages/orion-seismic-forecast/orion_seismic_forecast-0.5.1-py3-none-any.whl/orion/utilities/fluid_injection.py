# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
fluid_injection.py
-----------------------
"""

import numpy as np
# import pandas as pd
from datetime import timedelta
import logging

logger = logging.getLogger('orion_logger') = logging.getLogger('orion_logger')

# TODO: Move fluid injection attribute functions to this file
# TODO: Move other functions out of this file


def calc_injection_parameters(df_fr, fForecastStart, fForecastEnd, fDt):
    """
    calculate cumulative fluid volume and incremental injection from start to end in fDt time bins

    @arg fForecastStart      year - month - day - hour - minute - second
    @arg fForecastEnd        year - month - day - hour - minute - second
    @arg fDt                 time bin in days
    @arg df_fr               Pandas injection
    @returns countFr_cumulative  step wise cumulative volume (tvec)
    @returns countFr_diff        difference vector of countFr_cumulative
    """

    tvec = create_tvec(fForecastStart, fForecastEnd, fDt)

    countFr_cumulative = []
    for ii in range(len(tvec) - 1):
        tp_fr = df_fr.where((df_fr['date'] >= tvec[ii]) & (df_fr['date'] <= tvec[ii + 1]))
        cE = np.max(tp_fr['fluid_volume_cumulative'])
        if ii > 1:
            # check that fluid volume doesn't decrease in case data is empty
            if cE < countFr_cumulative[ii - 1]:
                cE = countFr_cumulative[ii - 1]
        countFr_cumulative = np.append(countFr_cumulative, cE)
        countFr_diff = np.diff(countFr_cumulative)
    return countFr_cumulative, countFr_diff


def create_tvec(fForecastStart, fForecastEnd, fDt):
    """
    create a date vector from fForecastStart to fForecastEnd with fDt steps

    @arg fForecastStart description
    @arg fForecastEnd description
    @arg fDt description
    @returns tvec description
    """
    fForecastStart = pd.to_datetime(fForecastStart)
    fForecastEnd = pd.to_datetime(fForecastEnd)
    tvec = np.arange(fForecastStart, fForecastEnd, timedelta(days=fDt))
    return tvec


def calc_seismicity_rate(df_cat, minMag, fForecastStart, fForecastEnd, fDt):
    """
    calculate observed seismicity in seismicity cat from start to end in fDt time bins above minMag

    @arg fForecastStart  year - month - day - hour - minute - second
    @arg fForecastEnd    year - month - day - hour - minute - second
    @arg fDt             time bin in days
    @arg minMag          Magnitude of completness
    @arg df_cat          Pandas catalog, needs date and magnitude

    @returns countEv
    @returns countEv_cumulative

    example:
    countEv, countEv_cumulative = calc_seismicity_rate(df_cat, 0.9, ('2006-12-02-18-0-0'),('2006-12-23-18-0-0'), 0.25)
    """

    tvec = create_tvec(fForecastStart, fForecastEnd, fDt)
    countEv = list()
    for ii in range(len(tvec) - 1):
        tp_cat = df_cat.where((df_cat['mag'] >= minMag) & (df_cat['date'] >= tvec[ii])
                              & (df_cat['date'] <= tvec[ii + 1]))
        cE = tp_cat['date'].count()
        countEv = np.append(countEv, cE)
    countEv_cumulative = np.cumsum(countEv)

    return countEv, countEv_cumulative


def bmemag(df_cat):
    """
    calculate the b-value and standard deviation
    values set to Nan if input catalog less than 10 entires

    @arg df_cat
    @returns b_value
    @returns std_one
    @returns a_value
    """
    if not len(df_cat) > 10:
        logger.warning('Input catalog too short')
        b_value = np.nan
        a_value = np.nan
        std_one = np.nan
    else:
        mag = df_cat['mag']
        maxmag = max(mag)
        mima = min(mag)
        if mima > 0:
            mima = 0
    # calculate the mean magnitude, b(mean) and std
        n = len(mag)
        mean_m1 = np.mean(mag)
        b_value = (1 / (mean_m1 - min(mag - 0.05))) * np.log10(np.exp(1))
        std_one = (np.sum((mag - mean_m1)**2)) / (n * (n - 1))
        std_one = np.sqrt(std_one)
        std_one = 2.30 * std_one * b_value**2    # standard deviation
        a_value = np.log10(len(mag)) + b_value * min(mag)
    return b_value, std_one, a_value


def calc_bvalue(df_cat, minMag, fForecastStart, fForecastEnd, fDt):
    """
    function to calculate the mean b value a b-value with time from fForecastStart
    to fForecastEnd with fDt time steps

    @arg df_cat          catalog with time and magnitude
    @arg minMag          completeness magnitude (minimum magnitude)
    @arg fForecastStart  year - month - day - hour - minute - second
    @arg fForecastEnd    year - month - day - hour - minute - second
    @arg fDt             time bin in days
    @returns b_value         mean b value for the whole sequence
    @returns b_value_time    b value with time

    example:
    b_value, b_value_time =calc_bvalue(df_cat, 0.9, ('2006-12-02-18-0-0'),('2006-12-23-18-0-0'), 0.25)
    """
    tvec = create_tvec(fForecastStart, fForecastEnd, fDt)
    tp_cat = df_cat.where((df_cat['mag'] >= minMag) & (df_cat['date'] <= fForecastEnd))
    tp_cat = tp_cat.dropna()

    [b_value, std_bvalue, a_value] = bmemag(tp_cat)

    b_value_time = []
    for ii in range(len(tvec) - 1):
        tp_cat = df_cat.where((df_cat['mag'] >= minMag) & (df_cat['date'] >= tvec[ii])
                              & (df_cat['date'] <= tvec[ii + 1]))
        tp_cat = tp_cat.dropna()
        if len(tp_cat) <= 10:
            # if tp_cat too short, b_value_time = mean b_value
            bv = b_value
        else:
            [bv, std_bvalue, a_value] = bmemag(tp_cat)
        b_value_time = np.append(b_value_time, bv)

    return b_value, b_value_time


def calc_seismogenic_index(df_cat, df_fr, minMag, fForecastStart, fForecastEnd, fDt, opt, fixB):
    """
    calculate the seismogenic index with different options

    @arg df_cat          seismic catalog
    @arg df_fr           injection catalog with cumulative volume and time
    @arg minMag          minimum Magnitude
    @arg fForecastStart,
    @arg fForecastEnd
    @arg fDt
    @arg opt             Option for seismogenic index calculation
                                                 fB = fixed bvalue
                                                 mB = mean bvalue
                                                 uB = updated bvalue
    @arg fixB            b value for option fB. Dummy value for other options
    @returns seismoIdx
    """
    b_value, b_value_time = calc_bvalue(df_cat, minMag, fForecastStart, fForecastEnd, fDt)
    countEv, countEv_cumulative = calc_seismicity_rate(df_cat, minMag, fForecastStart, fForecastEnd, fDt)
    countFr_cumulative = calc_injection_parameters(df_fr, fForecastStart, fForecastEnd, fDt)
    tvec = create_tvec(fForecastStart, fForecastEnd, fDt)

    seismoIdx = list()
    seismoIdx = np.append(seismoIdx, 0.5)
    if opt == 'fB':
        for ip in range(1, len(countFr_cumulative)):
            eu = np.log10(countEv_cumulative[ip]) - np.log10(countFr_cumulative[ip]) + fixB * minMag
            seismoIdx = np.append(seismoIdx, eu)
    elif opt == 'mB':
        for ip in range(1, len(countFr_cumulative)):
            eu = np.log10(countEv_cumulative[ip]) - np.log10(countFr_cumulative[ip]) + b_value * minMag
            seismoIdx = np.append(seismoIdx, eu)
    elif opt == 'uB':
        for ip in range(1, len(countFr_cumulative)):
            eu = np.log10(countEv_cumulative[ip]) - np.log10(countFr_cumulative[ip]) + b_value_time[ip] * minMag
            seismoIdx = np.append(seismoIdx, eu)

    return seismoIdx
