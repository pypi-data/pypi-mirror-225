# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
reasenberg_jones_model.py
---------------------------
"""

import numpy as np
import datetime
from scipy import integrate
from orion.forecast_models import forecast_model_base

# TODO: Place the important methods for the forecast model into this class structure


class ReasenbergJonesModel(forecast_model_base.ForecastModel):
    """
    Reasenberg-Jones forecast model

    Attributes:
        active (bool): Flag to indicate whether the model is active
        pressure_method (str): Pressure calculation method
        forecast_time (ndarray): Time values for forecast calculation
    """

    def set_class_options(self, **kwargs):
        """
        Reasenberg Jones model initialization

        """
        super().set_class_options(**kwargs)
        self.long_name = 'Reasenberg and Jones'
        self.short_name = 'RJ'

    def forecast_if_catalog(self):
        """
        Forecasting model if a catalog is active
        """
        pass

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        self.logger.warning('    (setting forecast to random array)')
        N = grid.shape
        self.temporal_forecast = np.cumsum(np.random.randint(0, 5, N[3]))
        self.spatial_forecast = np.random.randn(*N)

        return self.temporal_forecast, self.spatial_forecast

    """
    def old_method(self, seismic_catalog):
        # Use the data provided by the forecast manager
        # cat_file = '%s/Basel_cat.dat' % (test_data.__path__[0])
        # a = file_io.read_zmap_catalog(cat_file)
        a = seismic_catalog

        sForecastRate = calc_RJ(5.5, 5, 7, -1.6, 1, 1.2, 0.05, 12, 0)

        fMinMagRange = 0.5
        fMaxMagRange = 3.5
        dmag = 0.1
        magbin = 3
        fcbiMinM = 0.5
        fcbiMaxM = 3.5
        fAvalue = -1.67
        fBvalue = 0.91
        fPvalue = 1.08
        fCvalue = 1
        fForecastTime = 6 / 24
        fForecastStart = 0.01
        fForecastEnd = 7
        fDt = 0.2

        k = 0
        sForecastRate = list()
        frange = np.arange(fMinMagRange, fMaxMagRange, dmag)
        for fmagmin in frange:
            fMinMag = fmagmin
            fMaxMag = fmagmin + magbin

            date_start = a.date[0]

            # setting all variables to zero before starting
            FcRates = list()
            FcRt = list()
            FcRtfcbi = list()
            FcRatesfcbi = list()
            ForeRates = list()
            ForeRatesfcbi = list()

            # calculate all rates, probabilities for fMinMag to fMaxMag
            # get the whole range of the input catalogue
            MagRangeCat = np.arange(np.min(a.mag), np.max(a.mag), 0.1)

            for mcat in MagRangeCat:
                timesteps = np.arange(fForecastStart, fForecastEnd, fDt)
                for Ts in timesteps:
                    FcRt.append(calc_RJ(mcat, fMinMag, fMaxMag, fAvalue, fBvalue, fPvalue, fCvalue, fForecastTime, Ts))
                    #        repeat for second forcasted magnitude range
                    FcRtfcbi.append(
                        calc_RJ(mcat, fcbiMinM, fcbiMaxM, fAvalue, fBvalue, fPvalue, fCvalue, fForecastTime, Ts))

                for index, ev in a.iterrows():
                    fMainMag = ev.mag
                    date_rel = (ev.date - date_start).total_seconds() / 86400

                    #          %difference between hrel and start of forecast
                    #          %hrel=hrel_1-fForecastStart;
                    hrel = date_rel - fForecastStart
                    #          %search FcRt for Magnitude fMainMag (+0.01, -0.01 because of
                    #          %Matlab...)

                    # rm=(FcRt(:,4)<fMainMag+0.01 & FcRt(:,4)>fMainMag-0.01);
                    # FcRtm=FcRt(rm,:);
                    FcRt = np.array(FcRt)
                    FcRtm = FcRt[(FcRt[:, 3] < (fMainMag + 0.01)) & (FcRt[:, 3] > (fMainMag - 0.01)), :]

                    #          %adjust time according starttime
                    FcRtm[:, 1] = FcRtm[:, 1] + hrel
                    FcRates.append(FcRtm)

                    #          %repeat for second Magnitudes
                    #          %search FcRt for Magnitude fMainMag (+0.01, -0.01 because of
                    #          %Matlab...)
                    # rm=(FcRtfcbi(:,4)<fMainMag+0.01 & FcRtfcbi(:,4)>fMainMag-0.01);
                    # FcRtmfcbi=FcRtfcbi(rm,:);
                    FcRtfcbi = np.array(FcRtfcbi)
                    FcRtmfcbi = FcRtfcbi[(FcRtfcbi[:, 3] < (fMainMag + 0.01)) & (FcRtfcbi[:, 3] > (fMainMag - 0.01)), :]

                    #         %adjust time according starttime
                    FcRtmfcbi[:, 1] = FcRtmfcbi[:, 1] + hrel
                    FcRatesfcbi.append(FcRtmfcbi)

                #      %bin rates in time bins
                rbs = np.arange(fForecastStart, fForecastEnd, fDt)
                for rb in rbs:
                    binrate = np.sum(FcRates[(FcRates[:, 1] >= rb) & (FcRates[:, 1] <= rb + fDt), 0])
                    binprob = 1 - np.exp(-1 * binrate)
                    ForeRates.append([binrate, rb + fDt, binprob, 'nan', 'nan'])
                for rb in rbs:
                    binratefcbi = np.sum(FcRatesfcbi[(FcRatesfcbi[:, 1] >= rb) & (FcRatesfcbi[:, 1] <= rb + fDt), 0])
                    binprobfcbi = 1 - np.exp(-binratefcbi)
                    ForeRatesfcbi.append([binratefcbi, rb + fDt, binprobfcbi])

                #     %search for actual events
                date_mk = (a[(a['mag'] >= fMinMagRange) & (a['mag'] <= fMaxMagRange)].date - date_start)
                date_mk = np.array(date_mk.apply(datetime.timedelta.total_seconds)) / 86400
                rate_obs = list()

                for hk in range(len(ForeRates[:, 1])):
                    sr_d = np.where((date_mk <= ForeRates[hk, 1]) & (date_mk >= ForeRates[hk, 1] - fForecastTime))
                    rob = len(sr_d)
                    rate_obs.append(rob)

                ForeRates[:, 3] = rate_obs
                ForeRates[:, 4] = ForeRates[:, 0] - ForeRates[:, 3]

                sForecastRate[k].magbin = [fMinMag, fMaxMag]
                sForecastRate[k].rates = ForeRates
                sForecastRate[k].ratesfcbi = ForeRatesfcbi
                k = k + 1
    """


def calc_RJ(fMainMag, fMinMag, fMaxMag, fAvalue, fBvalue, fPvalue, fCvalue, fForecastTime, fForecastStart):
    """
    Old method to calculate rates of aftershocks and probabilities within time

    Args:
        fMainMag (float): main shock magnitude
        fMinMag (float): minimum magnitude to forecast rates for
        fMaxMag (float): maximum magnitude to forecast rates for
        dmag (float): Magnitude Step for integration
        fAvalue (float): Generic a-value
        fBvalue (float): Generic b-value
        fPvalue (float): Generic p-value
        fCvalue (float): Generic c-value
        fForecastTime (float): Length of forecast window (days)
        fForcastStart (float): Start of forcast window after the main shock (days)

    Returns:
        tuple: [Forecast Rate, Start Time, Probabilities, mainMag]

    Example:
        sForecastRate = calc_RJ(5.5,5, 7, -1.6, 1, 1.2, 0.05, 12, 0)

    """
    ForecastRates = integrate.dblquad(
        lambda s, m: 10**(fAvalue + fBvalue * (fMainMag - m)) * (s + fCvalue)**(-1 * fPvalue), fMinMag, fMaxMag,
        lambda s: fForecastStart, lambda s: fForecastStart + fForecastTime)

    #    %Probability that event from minMag to maxmag happens at within time
    #    %Forecaststart-Forecasttime
    vProbRates = 1 - np.exp(-1 * ForecastRates[0])
    ForecastRates = [ForecastRates[0], fForecastStart, vProbRates, fMainMag]
    return ForecastRates


# def calc_rateprob(fMinMagRange,fMaxMagRange,dmag, magbin, fcbiMinM,fcbiMaxM,fAvalue,fBvalue,fPvalue,fCvalue,fForecastTime,fForecastStart, fForecastEnd,fDt, a):
#     %
#     % two examples if its not called from call_calc_rateprob
#     %[sForecastRate]= calc_rateprob(0.5,3.5,0.1, 3, 0.5,3.5,-1.67,0.91,1.08,1,6/24,0.01,7,0.1,a);
#     %[sForecastRate]= calc_rateprob(0.9,1  ,0.1, 0.1, 1,1.2,-0.6,1.4,1.0,1,6,0.5,10,0.1,a);
#     %
#
#     %Function to calculate rates of aftershocks and probabilities within time
#     % fForecastTime - fForecastStart. fForecastStart must be a time range
#     %
#     % Input:
#
#     %fMinMagRange,fMaxMagRange,dmag, magbin, fcbiMinM,fcbiMaxM,fAvalue,fBvalue,fPvalue,fCvalue,fForecastTime,fForecastStart, fForecastEnd,fDt,a);
#     % fMinMagRange : minimum magnitude to forecast rates for
#     % fMaxMagRange : maximum magnitude to forecast rates for
#     % dmag    : Magnitude Step for integration
#     % magbin  : Size of Magnitude bin
#     % fcbiMinM:    Second minimum magnitude
#     % fcbiMaxM:    Seconc maximum magnitude
#     % fAvalue : a-value  (from Reasenberg&Jones, not GutenbergRichter!)
#     % fBvalue : b-value
#     % fPvalue : p-value
#     % fCvalue : c-value
#     % fForecastTime : Length of forecast window (days)
#     % fForcastStart : Start of forcast window after the main shock (days)
#     % fForcastEnd   : End of forcast window after the main shock (days)
#     % fDt :  Time step for integration
#     % catalog : input catalogue
#     %
#     % Output: sForecastRate     structure with
#     %           magbin:     Magnitude bin for which rates are calculated
#     %           rates:      Forecast Rate; Start Time; Probabilities; Observed Rates; Diference (:,1) and (:,4)
#     %

#    return sForecastRate

# def call_calc_rateprob(amtpar, fMinMagRange,fMaxMagRange,dmag, magbin,fcbiMinM,fcbiMaxM, fAvalue,fBvalue,fPvalue,fCvalue,fForecastTime,fForecastStart, fForecastEnd,fDt, minPar, maxPar, dpar, minPar2, maxPar2, dpar2,parType,a):
# # %
# # %
# # %Function call_calc_rateprob(amtpar, fMinMagRange,fMaxMagRange,dmag, magbin, fAvalue,fBvalue,fPvalue,fCvalue,fForecastTime,fForecastStart, fForecastEnd,fDt, minPar, maxPar, dpar, minPar2, maxPar2, dpar2,parType,a);
# # %
# # % Example
# # %[sForecastRate]= call_calc_rateprob(2, 0.5,3.5,3,3,0.5,3.5,-0.5,1,1.2,0.05,6/24,0.01, 10,1, 0.8, 1.6, 0.1, -2, -0.5, 0.1,'pa',a);
# # %
# # %Input:
# # % amtpar  : Amount of parameters
# # % fMinMag : minimum magnitude to forecast rates for
# # % fMaxMag : maximum magnitude to forecast rates for
# # % dmag    : Magnitude Step for integration
# # % magbin  : Size of Magnitude bin
# # % fcbiMinM: Second minimum magnitude (if two mag ranges should be
# # %           calculated at once
# # % fcbiMaxM: Seconc maximum magnitude
# # % fAvalue : Generic a-value (not a value from G/R!, but from
# # %                           Reasenberg&Jones 1989)
# # % fBvalue : Generic b-value
# # % fPvalue : Generic p-value
# # % fCvalue : Generic c-value
# # % fForecastTime : Length of forecast window (days)
# # % fForcastStart : Start of forcast window after the main shock (days)
# # % fForcastEnd   : End of forcast window after the main shock (days)
# # % fDt :  Time step for integration
# # % minPar, maxPar,dpar : parameter range
# # %                       if amtpar = 1, second range can be bogus paramaters, first range counts
# # %                       if amtpar = 2, order either p a or c a or p c and
# # %                       then defining in parType
# # % parType :     if amtpar = 1, a,p or c
# # %               if amtpar = 2, pa, ca, or pc
# # % a       : input catalogue
# # %
# # %
# # %Output:
# # % sForecastRate      structure with
# # %           magbin:     Magnitude bin for which rates are calculated
# # %           rates:      Forecast Rate; Start Time; Probabilities; Observed Rates; Diference (:,1) and (:,4)
# # %           par:        parameter 1
# # %           par2:       parameter 2
# # %           partype:    which parameters were varried
# #
#     sForecastRate=[];
#     # only one parameter to calculate
#     if amtpar==1:
#  ct=1
#  par=np.arange(minPar, maxPar, dpar)
#  for pk in par:
#      if parType=='c':
#          Ratetmp = calc_rateprob(fMinMagRange, fMaxMagRange, dmag, magbin, fcbiMinM, fcbiMaxM, fAvalue, fBvalue, fPvalue, par[pk], fForecastTime, fForecastStart, fForecastEnd, fDt, a)
#
#          sRate[pk].rates=Ratetmp.rates
#          sRate[pk].magbin=Ratetmp.magbin
#          sRate[pk].parval=par[pk]
#          sRate[pk].partype='c'
#      elif parType=='p':
#          Ratetmp = calc_rateprob(fMinMagRange, fMaxMagRange, dmag, magbin, fcbiMinM, fcbiMaxM, fAvalue, fBvalue, par[pk], fCvalue, fForecastTime, fForecastStart, fForecastEnd, fDt, a);
#          sRate[pk].rates=Ratetmp.rates
#          sRate[pk].magbin=Ratetmp.magbin
#          sRate[pk].parval=par[pk]
#          sRate[pk].partype='p'
#      elif parType=='a':
#          Ratetmp = calc_rateprob(fMinMagRange, fMaxMagRange, dmag, magbin, fcbiMinM, fcbiMaxM, par[pk], fBvalue, fPvalue, fCvalue, fForecastTime, fForecastStart, fForecastEnd, fDt, a);
#          sRate[pk].rates=Ratetmp.rates;
#          sRate[pk].ratesfcbi=Ratetmp.ratesfcbi;
#          sRate[pk].magbin=Ratetmp.magbin;
#          sRate[pk].parval=par[pk];
#          sRate[pk].partype='a';
#
#        # sForecastRate=[sForecastRate sRate];
#
# #     elseif amtpar==2
#        #
#        #
#        #
#        #  par=minPar:dpar:maxPar;
#        #
#        #  par2=minPar2:dpar2:maxPar2;
#        #
#        #
#        #
#        #  for ik=1:length(par)
#        #      %loop around first parameter first, then determining what parameters and loop over second parameter
#        #
#        #      if strcmp(parType,'pa')
#        #
#        #          parfor pk=1:length(par2)
#        #              [Ratetmp]= calc_rateprob(fMinMagRange,fMaxMagRange,dmag, magbin,fcbiMinM,fcbiMaxM, par2(pk),fBvalue,par(ik),fCvalue,fForecastTime,fForecastStart, fForecastEnd,fDt,a);
#        #              srates(pk).rates=Ratetmp.rates;
#        #              srates(pk).magbin=Ratetmp.magbin;
#        #              srates(pk).par=par(ik);
#        #              srates(pk).par2=par2(pk);
#        #              srates(pk).partype='pa';
#        #          end
#        #
#        #      elseif strcmp(parType,'ca')
#        #          parfor pk=1:length(par2)
#        #              [Ratetmp]= calc_rateprob(fMinMagRange,fMaxMagRange,dmag, magbin,fcbiMinM,fcbiMaxM, par2(pk),fBvalue,fPvalue,par(ik),fForecastTime,fForecastStart, fForecastEnd,fDt,a);
#        #              srates(pk).rates=Ratetmp.rates;
#        #              srates(pk).magbin=Ratetmp.magbin;
#        #              srates(pk).par=par(ik);
#        #              srates(pk).par2=par2(pk);
#        #              srates(pk).partype='ca';
#        #          end
#        #      elseif strcmp(parType,'pc')
#        #          parfor pk=1:length(par2)
#        #              [Ratetmp]=calc_rateprob(fMinMagRange,fMaxMagRange,dmag, magbin,fcbiMinM,fcbiMaxM, fAvalue,fBvalue,par(ik),par2(pk),fForecastTime,fForecastStart, fForecastEnd,fDt,a);
#        #              srates(pk).rates=Ratetmp.rates;
#        #              srates(pk).magbin=Ratetmp.magbin;
#        #              srates(pk).par=par(ik);
#        #              srates(pk).par2=par2(pk);
#        #              srates(pk).partype='pc';
#        #          end
#        #
#        #      end
#        #      disp(num2str(par(ik)))
#        #      sForecastRate=[sForecastRate srates];
#        #      %ct=ct+1;
#        #      %end
#        #
#        #  end

# call_calc_rateprob(2, 0.5,3.5,3,3,0.5,3.5,-0.5,1,1.2,0.05,6/24,0.01, 10,1, 0.8, 1.6, 0.1, -2, -0.5, 0.1,'p',a);
# return sForecastRate
