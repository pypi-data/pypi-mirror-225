# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
timestamp_conversion.py
-----------------------
"""

import time
import datetime
import re
import logging
import numpy as np

time_formats = {
    'dd/mm/yyyy': {
        'conversion': '%d/%m/%Y',
        'pattern': r'\d{2}\/\d{2}\/\d{4}'
    },
    'dd/mm/yyyy hh:mm:ss': {
        'conversion': '%d/%m/%Y %H:%M:%S',
        'pattern': r'\d{2}\/\d{2}\/\d{4} \d{2}\:\d{2}\:\d{2}'
    },
    'epoch': {
        'conversion': '',
        'pattern': r'[\d]*([\d]\.?|\.[\d])[\d]*([eE][-+]?[\d]+|\s*)'
    }
}

time_units = f"({' | '.join(time_formats.keys())})"
logger = logging.getLogger('orion_logger')


def convert_timestamp(t_input):
    # logger.debug('Converting timestamp: %s' % (t_input))
    t_output = -1e99
    for k in time_formats.keys():
        if re.fullmatch(time_formats[k]['pattern'], t_input):
            if len(time_formats[k]['conversion']):
                t_output = datetime.datetime.strptime(t_input, time_formats[k]['conversion']).timestamp()
            else:
                t_output = float(t_input)

    if (t_output < -1e98):
        logger.warning(f'Timestamp entry not converted: {t_input}')
        logger.warning('Setting value to current time')
        t_output = datetime.datetime.now().timestamp()

    return t_output


def get_current_time_string():
    return get_time_string(time.time())


def get_time_string(t_input):
    return time.strftime('%d/%m/%Y', time.localtime(t_input))


def get_time_str_pycsep(t_input):
    return datetime.datetime.fromtimestamp(t_input).strftime('%Y-%m-%dT%H:%M:%S.%f')


def convert_time_arrays(year, month, day, hour, minute, second):
    logger.debug('Converting timestamp arrays')
    N = len(year)
    epoch = np.zeros(N)
    for ii in range(N):
        t = datetime.datetime(int(year[ii]), int(month[ii]), int(day[ii]), int(hour[ii]), int(minute[ii]))
        epoch[ii] = float(t.timestamp()) + second[ii]
    return epoch
