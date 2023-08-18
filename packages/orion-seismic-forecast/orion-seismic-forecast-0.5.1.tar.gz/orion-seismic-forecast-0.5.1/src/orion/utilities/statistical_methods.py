# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
statistical_methods.py
--------------------------------------
"""

import numpy as np


def poisson_probability(forecast_time, forecast_number, b_value, magnitude_completeness, magnitude_thresholds,
                        forecast_duration):
    """
    Compute the time dependent probability of an event M > magnitude_thresholds
    in the given time window using b-values, magnitude_completeness, and total
    number of events from the observed catalog during the fitting period

    Attributes:
        forecast_time (np.array): time series associated with forecast_number
             (default unit is seconds)
        forecast_number (np.array): forecasted number of events as a function of time
            listed in forecast_time
        magnitude_thresholds (np.array): Magnitude of events of interest.
            Compute probability of M>magnitude_thresholds
        forecast_duration (integer): forecast_durationation of the probability
            calculation period (same units a forecast_time)
        magnitude_completeness (integer): Magnitude of completeness of
            the events in eqs, compute with other means
    Returns:
        np.array of proababilities of an event M>magnitude_thresholds will occur in the time 'forecast_duration' for all magnitude_thresholds
    """

    N = np.amax(forecast_number) - np.amin(forecast_number)
    dT = np.amax(forecast_time) - np.amin(forecast_time)
    probability = np.zeros(len(magnitude_thresholds))

    if (dT > 0.0):
        for ii in range(len(magnitude_thresholds)):
            lambda_M = forecast_duration * ((N / dT) * 10**(-b_value *
                                                            (magnitude_thresholds[ii] - magnitude_completeness)))
            pr = 100 * (1 - np.exp(-lambda_M))
            probability[ii] = round(pr, 1)

    return (probability)
