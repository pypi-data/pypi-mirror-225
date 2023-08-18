# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
coupled_coulomb_rate_state_model.py
--------------------------------------
"""

from orion.forecast_models import forecast_model_base
import numpy as np
from orion.managers.manager_base import recursive


class CRSModel(forecast_model_base.ForecastModel):
    """
    CRS forecast model

    Attributes:
        active (bool): Flag to indicate whether the model is active
        pressure_method (str): Pressure calculation method
        forecast_time (ndarray): Time values for forecast calculation
    """

    def set_class_options(self, **kwargs):
        """
        CRS model initialization

        """
        # Call the parent's setup
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.short_name = 'CRS'
        self.long_name = 'Coupled Coulomb Rate-State Model'

        # Forecast variables
        self.mu = 0.73
        self.background_rate_input = 1.36    # events/year
        self.tectonicShearStressingRate_input = 3.5e-4    # MPa/year
        self.tectonicNormalStressingRate_input = 0    # MPa/year
        self.rate_coefficient = 0.00264
        self.alpha = 0.155
        self.sigma_input = 30.0    # MPa
        self.biot = 0.3
        self.rate_factor_input = 163.7424    # 1/MPa

        self.sigma = 1.0
        self.tectonicShearStressingRate = 1.0
        self.tectonicNormalStressingRate = 1.0
        self.background_rate = 1.0
        self.rate_factor = 1.0
        self.enable_clustering = False

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        super().set_gui_options(**kwargs)

        # Add the variable to the gui
        self.gui_elements['mu'] = {
            'element_type': 'entry',
            'label': u'\u03BC: Coefficient of Friction',
            'units': '(0-1)',
            'position': [4, 0]
        }

        self.gui_elements['sigma_input'] = {
            'element_type': 'entry',
            'label': 'Normal Stress',
            'position': [4, 1],
            'units': '(MPa)'
        }

        self.gui_elements['rate_coefficient'] = {
            'element_type': 'entry',
            'label': 'Rate-coefficient',
            'position': [5, 0]
        }

        self.gui_elements['biot'] = {'element_type': 'entry', 'label': 'Biot-Coefficient', 'position': [5, 1]}

        self.gui_elements['alpha'] = {
            'element_type': 'entry',
            'label': u'\u03B1: [Normal Stress Dependency]',
            'position': [6, 0],
            'units': '(0-\u03BC)'
        }

        self.gui_elements['tectonicShearStressingRate_input'] = {
            'element_type': 'entry',
            'label': 'Tectonic Shear Stressing Rate',
            'position': [6, 1],
            'units': '(MPa/year)'
        }

        self.gui_elements['tectonicNormalStressingRate_input'] = {
            'element_type': 'entry',
            'label': 'Tectonic Normal Stressing Rate',
            'position': [7, 0],
            'units': '(MPa/year)'
        }

        self.gui_elements['background_rate_input'] = {
            'element_type': 'entry',
            'label': 'Background Seismicity Rate',
            'position': [7, 1],
            'units': '(events/year)'
        }

        self.gui_elements['rate_factor_input'] = {
            'element_type': 'entry',
            'label': 'Rate Scaling Factor',
            'position': [8, 0],
            'units': '(1/MPa)'
        }
        self.gui_elements['enable_clustering'] = {
            'element_type': 'check',
            'label': 'Enable Clustering Effects',
            'position': [8, 1]
        }

    @recursive
    def process_inputs(self):
        """
        Process any required gui inputs
        """
        mpa_yr2pa_s = 1e6 / 365.25 / 86400    # MPa/year to Pa/s
        self.sigma = self.sigma_input * 1e6    # Pa
        self.tectonicShearStressingRate = self.tectonicShearStressingRate_input * mpa_yr2pa_s    # Pa/s
        self.tectonicNormalStressingRate = self.tectonicNormalStressingRate_input * mpa_yr2pa_s    # Pa/s
        self.background_rate = self.background_rate_input / 365.25 / 86400    # event/second
        self.rate_factor = self.rate_factor_input / 1e6    # 1/Pa

    def computeSigmaEffective(self, pressure):
        """
        Effective (time-dependent) normal stress that varies with pressure

        Args:
            sigma (float): initial normal stress (Pa)
            biot (float): biot coefficient
            pressure (np.array): pore-fluid pressure time series at a point (Pa)

        Returns:
            np.array: effective normal stress time series
        """
        return (self.sigma - (self.biot * pressure))

    def computeCoulombStressingRate(self, pressureRate):
        """
        Effective (time-dependent) normal stress that varies with pressure

        Args:
            pressureRate (np.array): pore-fluid pressurization rate time
                series at a point (MPa)

        Returns:
            np.array: Coulomb stressing rate time series
        """
        return (self.tectonicShearStressingRate - ((self.mu - self.alpha) *
                                                   (self.tectonicNormalStressingRate - pressureRate)))

    def instantRateChange(self, static_coulomb_stress_change, background_rate, rate_coefficient, sigma_effective):
        """
        Instantaneous change in Rate (R) due to step change in Coulomb stress

        Args:
            static_coulomb_stress_change (float): Coulomb stress step (Pa by default)
            background_rate (float): long-term background seismicity rate before stress step (seconds by default)
            rate_coefficient (float): rate-coefficient in rate-state formulation
            sigma_effective (np.array): effective normal stress (Pa; sigma_effective = sigma - biot*pressure)

        Returns:
            float: Instantaneous change in rate
        """
        asigma = rate_coefficient * sigma_effective
        return (background_rate * np.exp(static_coulomb_stress_change / asigma))

    def interseismicRate(self, forecast_time, eta, coulomb_stressing_rate, rate_at_prev_step, rate_coefficient,
                         sigma_effective):
        """
        Evolution of the Rate during a time of constant stressing rate

        Args:
            forecast_time (np.array): Times at which number should be computed (units:
                            same as the time units in sigma_effective; seconds by default)
            eta (float): reference stressing rate divided by background rate (steady
                         event rate that would be produced by constant stressing at the
                         reference stressing rate) (units: stress/event with stress
                         in same units as the stress units in sigma_effective; Pa/second by default)
            coulomb_stressing_rate(np.array): Constant Coulomb stressing rate (units: same stress units
                               as used in eta, same time units as t; Pa/second by default)
            rate_at_prev_step (float): event rate at the previous time step (units: events/time, same time units
                        as forecast_time (seconds by default))
            rate_coefficient (float): rate-coefficient in rate-state formulation
            sigma_effective (np.array): effective normal stress (Pa; sigma_effective = sigma - biot*pressure)

        Returns:
            np.array: interseismic rate
        """
        asigma = rate_coefficient * sigma_effective
        if (coulomb_stressing_rate == 0):
            return (1 / (1 / rate_at_prev_step + eta * forecast_time / asigma))
        else:
            x = np.exp(-coulomb_stressing_rate * forecast_time / asigma)
            return (1 / (eta / coulomb_stressing_rate + (1 / rate_at_prev_step - eta / coulomb_stressing_rate) * x))

    def interseismicNumber(self, forecast_time, eta, coulomb_stressing_rate, rate_at_prev_step, rate_coefficient,
                           sigma_effective):
        """
        Compute expected total number of events during a time of constant stressing rate

        Args:
           forecast_time (np.array): np.array of times at which number should be computed
                         (units: same as the time units in sigma_effective; seconds by default)
           eta (float): reference stressing rate divided by background rate (steady
                        event rate that would be produced by constant stressing at the
                        reference stressing rate) (units: stress/event with stress
                        in same units as the stress units in sigma_effective; Pa/second by default)
           coulomb_stressing_rate(np.array): np.array of constant Coulomb stressing rate (units: same stress units
                                             as used in eta, same time units as forecast_time; Pa/second by default)
           rate_at_prev_step (float): event rate at the previous time step (units: events/time, same time units
                                      as forecast_time (seconds by default))
           rate_coefficient (float): rate-coefficient in rate-state formulation
           sigma_effective (np.array): effective normal stress (Pa; sigma_effective = sigma - biot*pressure)

        Returns:
           np.array: interseismic number
        """
        asigma = rate_coefficient * sigma_effective
        if (coulomb_stressing_rate == 0):
            return ((asigma / eta) * np.log(1 + rate_at_prev_step * eta * forecast_time / asigma))
        else:
            x = np.exp(coulomb_stressing_rate * forecast_time / asigma)
            x *= (rate_at_prev_step * eta / coulomb_stressing_rate)
            return ((asigma / eta) * np.log((1 - rate_at_prev_step * eta / coulomb_stressing_rate) + x))

    def rateEvolution(self, forecast_time, large_event_times_in_forecast, static_coulomb_stress_change,
                      coulomb_stressing_rate, background_rate, rate_factor, rate_coefficient, sigma_effective):
        """
        Calculate the earthquake rate for all times passed into t.
        t and large_event_times_in_forecast  must all have the same units of time.
        for consistency, we will use "years" as the standard time unit.

        Instantaneous stress step vector (static_coulomb_stress_change) must be [length(sigma_effective) - 1]
        (stressing rate vector) beginning at the time of the first change

        Args:
            forecast_time (np.array): Times at which number should be computed
                          (units: same as the time units in sigma_effective; seconds by default)
            large_event_times_in_forecast (np.array): Times of the stress steps (seconds by default)
            static_coulomb_stress_change (np.array): Amplitude of the stress steps (+/- ; Pa by default)
                           must be the same length as large_event_times_in_forecast
            coulomb_stressing_rate: (np.array): constant Coulomb stressing rate (units: same stress units
                              as used in eta, same time units as t; Pa/second by default)
                              len(sigma_effective) must equal len(forecast_time)
            background_rate (float): Event rate at time forecast_time=0 (units: events/time, same time units
                        as forecast_time (seconds by default))
            rate_factor (float): 1/eta; the background seismicity rate divided by the background stressing rate
            rate_coefficient (float): rate-coefficient in rate-state formulation
            sigma_effective (np.array): effective normal stress (Pa; sigma_effective = sigma - biot*pressure)

        Returns:
           np.array: Rate evolution
        """
        R = np.empty(len(forecast_time))
        eta = 1 / rate_factor

        if (self.enable_clustering):
            if len(forecast_time) != len(sigma_effective):
                self.logger.error("forecast_time must be the same length as sigma_effective")
                return

            if len(static_coulomb_stress_change) != len(large_event_times_in_forecast):
                self.logger.error(
                    "large_event_times_in_forecast must be the same length as static_coulomb_stress_change")
                return

            # Separate the time array into individual periostatic_coulomb_stress_change defining the interseismic period
            # and the time of the stress steps
            index = np.digitize(forecast_time, bins=large_event_times_in_forecast, right=False)
            R[index == 0] = background_rate

            # Loop over all times, t, check if t[i] is the time of a stress step. If it is,
            # compute the instantaneous rate change. If it is not, then compute the gamma evolution
            # due to changes in sigma_effective
            for i in range(1, len(forecast_time)):
                if not (index[i] == index[i - 1]):
                    R[i] = self.instantRateChange(static_coulomb_stress_change[index[i - 1]], R[i - 1],
                                                  rate_coefficient, sigma_effective[i])
                else:
                    R[i] = self.interseismicRate(forecast_time[i] - forecast_time[i - 1], eta,
                                                 coulomb_stressing_rate[i], R[i - 1], rate_coefficient,
                                                 sigma_effective[i])
        else:
            R[0] = background_rate
            for i in range(1, len(forecast_time)):
                R[i] = self.interseismicRate(forecast_time[i] - forecast_time[i - 1], eta, coulomb_stressing_rate[i],
                                             R[i - 1], rate_coefficient, sigma_effective[i])
        return (R)

    def numberEvolution(self, forecast_time, large_event_times_in_forecast, static_coulomb_stress_change,
                        coulomb_stressing_rate, background_rate, rate_factor, rate_coefficient, sigma_effective):
        """
        Calculate the number of events for all times passed into forecast_time.
        forecast_time and large_event_times_in_forecast  must all have the same units of time.
        for consistency, we will use "seconds" as the standard time unit.

        Instantaneous stress step vector (static_coulomb_stress_change) must be [length(sigma_effective) - 1]
        (stressing rate vector) beginning at the time of the first change

        Args:
            forecast_time (np.array): Times at which number should be computed
                                      (units same as the time units in sigma_effective; seconds by default)
            large_event_times_in_forecast (np.array): Times of the stress steps (seconds by default)
            static_coulomb_stress_change (np.array): Amplitude of the stress steps (+/- ; Pa by default)
                                                     must be the same length as large_event_times_in_forecast
            coulomb_stressing_rate(np.array): Constant Coulomb stressing rate (units: same stress units
                                              as used in eta, same time units as t; Pa/second by default)
            background_rate (float): Event rate at time forecast_time=0 (units: events/time, same time units
                                     as forecast_time (seconds by default))
            rate_factor (float): 1/eta; the background seismicity rate divided by the background stressing rate
            rate_coefficient (float): rate-coefficient in rate-state formulation
            sigma_effective (np.array): effective normal stress (Pa; sigma_effective = sigma - biot*pressure,
                                        same length as forecast_time)

        Returns:
            np.array: Number evolution
        """
        N = np.empty(len(forecast_time))
        R = np.empty(len(forecast_time))
        eta = 1 / rate_factor

        if (self.enable_clustering):
            if len(forecast_time) != len(sigma_effective):
                # self.logger.error("forecast_time must be the same length as sigma_effective")
                return 0

            if len(static_coulomb_stress_change) != len(large_event_times_in_forecast):
                # self.logger.error("large_event_times_in_forecast must be the same length as static_coulomb_stress_change")
                return 0

            # Separate the time array into individual periostatic_coulomb_stress_change defining the interseismic period
            # and the time of the stress steps
            index = np.digitize(forecast_time, bins=large_event_times_in_forecast, right=False)

            useT = np.where(index == 0)
            R[useT] = background_rate
            N[useT] = background_rate * (forecast_time[useT] - forecast_time[0])

            # Loop over all forecast_times
            # 1) compute the instantaneous rate at the time of each large_events
            #    1a) use sigma_effective at the time of the large event
            # 2) compute the aftershock decay until the time of the next large event
            # 3) update the current rate (rCurrent) and nCurrent at the time step
            #    just before the next large event to be used in the next iteration
            #    3a) use the coulomb_stressing_rate and sigma_effective at the time step
            #       just before the next large event
            for i in range(1, len(forecast_time)):
                if not (index[i] == index[i - 1]):
                    R[i] = self.instantRateChange(static_coulomb_stress_change[index[i - 1]], R[i - 1],
                                                  rate_coefficient, sigma_effective[i])
                    N[i] = N[i - 1] + self.interseismicNumber(forecast_time[i] - forecast_time[i - 1], eta,
                                                              coulomb_stressing_rate[i], R[i - 1], rate_coefficient,
                                                              sigma_effective[i])
                else:
                    R[i] = self.interseismicRate(forecast_time[i] - forecast_time[i - 1], eta,
                                                 coulomb_stressing_rate[i], R[i - 1], rate_coefficient,
                                                 sigma_effective[i])
                    N[i] = N[i - 1] + self.interseismicNumber(forecast_time[i] - forecast_time[i - 1], eta,
                                                              coulomb_stressing_rate[i], R[i - 1], rate_coefficient,
                                                              sigma_effective[i])
        else:
            R[0] = background_rate
            N[0] = background_rate * (forecast_time[1] - forecast_time[0])

            for i in range(1, len(forecast_time)):
                R[i] = self.interseismicRate(forecast_time[i] - forecast_time[i - 1], eta, coulomb_stressing_rate[i],
                                             R[i - 1], rate_coefficient, sigma_effective[i])
                N[i] = N[i - 1] + self.interseismicNumber(forecast_time[i] - forecast_time[i - 1], eta,
                                                          coulomb_stressing_rate[i], R[i - 1], rate_coefficient,
                                                          sigma_effective[i])
        return (N)

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        # Estimate pressure in the xy plane at the center of the zgrid
        Nx = len(grid.x)
        Ny = len(grid.y)
        Nt = len(grid.t)
        self.forecast_time = grid.t.copy()

        if (self.enable_clustering):
            # Find events over magnitude 3
            target_magnitude = 3.2
            self.logger.info("Mininum target_magntiude is currently hard-coded, but should be exposed to the user")
            time_window = [44312204, 1.9 * 86400 * 365.25]    # Need to figure out a way to do this automatically
            self.logger.info(
                "Currently, the time period to look for the mainshocks is hard-coded and should be updated so that mainshocks above a given magnitude are automatically selected."
            )
            minimum_interevent_time = 0.02 * 86400 * 365.25
            self.logger.info(
                "Minimum time between mainshocks is currently hard-coded and COULD eventually be exposed to user or a default set."
            )
            seismic_catalog.set_slice(time_range=time_window,
                                      magnitude_range=[target_magnitude, 10],
                                      minimum_interevent_time=minimum_interevent_time)
            large_event_times_in_catalog = seismic_catalog.get_relative_time()
            # Add sample at the beginning of the pressure time series to account for offset from steady-state at the beginning of the operation
            # Note, this sample cannot be at grid.t[0]
            large_event_times_in_catalog = np.insert(large_event_times_in_catalog, 0, grid.t[1])
            self.logger.info(
                "Currently, a static stress step is being added at the beginning of the injection period (at the second time step) in order to offset seismicity rates above or below steady-state to account for unknown initial conditions."
            )
            # large_event_magnitudes = seismic_catalog.get_magnitude_slice()

            # Make sure to set the time of the large_event_times to the closest value
            # in the forecast_times
            large_event_times_in_forecast = []
            for time in large_event_times_in_catalog:
                large_event_times_in_forecast = np.append(
                    large_event_times_in_forecast, self.forecast_time[np.abs(time - self.forecast_time).argmin()])

            # Set the initial static Coulomb Stress change to be some fraction of
            # the event magnitude for now, but we may want to change this in the future.
            # Through trial and error, 0.1*M seems to work well.
            # coulomb_stress_change_by_percentage_magnitude = 0.1
            # static_coulomb_stress_change = coulomb_stress_change_by_percentage_magnitude*large_event_magnitudes
            static_coulomb_stress_change = np.array([-0.6477964, 0.5145350, 0.6200820]) * 1e6
            self.logger.info(
                "Using hard-coded static Coulomb stress changes now for the Cushing 2014 sequence. This will be updated when the parameter optimzation is added."
            )
        else:
            # self.forecast_time = grid.t[:-1]
            large_event_times_in_forecast = -999
            # large_event_magntiudes = -999
            static_coulomb_stress_change = -999

        self.spatial_forecast = np.zeros((Nt, Nx, Ny))
        for i in range(Nx):
            for j in range(Ny):
                sigma_effective = self.computeSigmaEffective(pressure.p_grid[i, j, 0, :])
                coulomb_stressing_rate = self.computeCoulombStressingRate(pressure.dpdt_grid[i, j, 0, :])
                c = self.numberEvolution(self.forecast_time, large_event_times_in_forecast,
                                         static_coulomb_stress_change, coulomb_stressing_rate, self.background_rate,
                                         self.rate_factor, self.rate_coefficient, sigma_effective)
                self.spatial_forecast[:, i, j] = c

        self.temporal_forecast = np.sum(self.spatial_forecast, axis=(1, 2))
        return self.temporal_forecast, self.spatial_forecast
