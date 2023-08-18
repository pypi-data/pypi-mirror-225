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

import logging

logger = logging.getLogger('orion_logger')


def load_TX_Railroad_Commission_data(epoch_start, epoch_stop):
    """
    Loads well data from Texas Railroad Commission site

    Args:
        epoch_start (int): Data request start time (seconds, epoch)
        epoch_stop (int): Data request stop time (seconds, epoch)

    Returns:
        dict: segment_data (or list of dicts)
    """
    logger.warning('TX_Railroad_Commission data not supported yet')
    segment_data = {}
    return segment_data
