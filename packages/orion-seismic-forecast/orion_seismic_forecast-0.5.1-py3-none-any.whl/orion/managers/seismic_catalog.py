# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
seismic_catalog.py
-----------------------
"""

from orion import optional_packages
from orion.managers import manager_base
from orion.utilities import timestamp_conversion, hdf5_wrapper, other
from orion.utilities.plot_config import gui_colors
from orion import _frontend
import numpy as np
from scipy import ndimage
import utm
import os
import datetime
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import collections

decluster_kwargs = {
    "gardner-knopoff": {
        "window": "uhrhammer"
    },
    "nearest-neighbor": {
        "d": 1.6,
        "eta_0": None,
        "alpha_0": 1.5,
        "use_depth": False,
        "seed": 0
    },
    "reasenberg": {
        "rfact": 10,
        "xmeff": None,
        "xk": 0.5,
        "tau_min": 1.0,
        "tau_max": 10.0,
        "p": 0.95
    },
}


class SeismicCatalog(manager_base.ManagerBase):
    """
    Structure for holding seismic catalog information

    Attributes:
        epoch (ndarray): Event timestamps (seconds)
        latitude (ndarray): Event latitudes (degrees)
        longitude (ndarray): Event longitudes (degrees)
        depth (ndarray): Event depths (m)
        utm_zone (int): UTM Zone for projection
        easting (ndarray): Eastings in UTM projection or local coordinates (m)
        northing (ndarray): Northings in UTM projection or local coordinates (m)
        magnitude (ndarray): Event magnitude magnitudes
        magnitude_bins (ndarray): magnitude magnitude bin edges
        cumulative_frequency (ndarray): magnitude magnitude exceedance per bin
        a_value (float): Gutenberg-Richter a-value
        b_value (float): Gutenberg-Richter b-value
        varying_b_time (ndarray): Times for estimating sub-catalog b-values
        varying_b_value (ndarray): Gutenberg-Richter b-values over time
        magnitude_completeness (float): Magnitude of completeness for catalog
        background_seismicity_rate (float): Background seismicity rate

    """

    def set_class_options(self, **kwargs):
        """
        Seismic catalog initialization function

        """

        # Set the shorthand name
        self.short_name = 'Seismic Catalog'

        # Source
        self.catalog_source = ''
        self.old_catalog_source = ''

        # Comcat filter
        self.use_comcat = 0
        self.comcat_utm_zone = -100
        self.comcat_start_time = 0
        self.comcat_end_time = 0
        self.comcat_min_magnitude = 0
        self.comcat_min_magnitude_old = -100
        self.comcat_min_latitude = 0
        self.comcat_max_latitude = 0
        self.comcat_min_longitude = 0
        self.comcat_max_longitude = 0
        self.comcat_request_complete = False

        # Time varying magnitude rate
        self.magnitude_rate_resolution = 100
        self.smoothing_kernal_sigma = '1.0'

        # Declustering
        self.type = ""
        self.decluster_algorithms = {k: False for k in decluster_kwargs}
        self.decluster_d = decluster_kwargs["nearest-neighbor"]["d"]
        self.decluster_rfact = decluster_kwargs["reasenberg"]["rfact"]
        self.decluster_xk = decluster_kwargs["reasenberg"]["xk"]
        self.decluster_tau_min = decluster_kwargs["reasenberg"]["tau_min"]
        self.decluster_tau_max = decluster_kwargs["reasenberg"]["tau_max"]
        self.decluster_p = decluster_kwargs["reasenberg"]["p"]

        # a, b-value methods
        self.a_value_default = 1.0
        self.b_value_default = 1.0
        self.b_value_min_points = 10
        self.b_value_methods = {
            "b-positive": gutenberg_richter_b_positive,
            "maximum likelihood estimate": gutenberg_richter_b_mle
        }
        self.current_b_value_method = "b-positive"

        # Mapping data loader methods to file extension
        self._loader_map = {
            ".dat": self.load_catalog_zmap,
            ".txt": self.load_catalog_txt,
            ".csv": self.load_catalog_csv,
            ".hdf5": self.load_catalog_hdf5,
        }

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        # Location
        self.latitude = np.zeros(0)
        self.longitude = np.zeros(0)
        self.depth = np.zeros(0)
        self.utm_zone = ''
        self.easting = np.zeros(0)
        self.northing = np.zeros(0)

        # Timing
        self.t_origin = 0.0
        self.epoch = np.zeros(0)
        self.data_slice = []
        self.time_range = [-1e99, 1e99]

        # Size, distribution
        self.magnitude = np.zeros(0)
        self.magnitude_bins = np.zeros(0)
        self.cumulative_frequency = np.zeros(0)
        self.a_value = 0.0
        self.b_value = 0.0
        self.varying_b_time = np.zeros(0)
        self.varying_b_value = np.zeros(0)
        self.magnitude_completeness = -3.0
        self.background_seismicity_rate = 0.0
        self.magnitude_range = [-1e99, 1e99]
        self.magnitude_rate = np.zeros(0)
        self.magnitude_rate_time = np.zeros(0)

        # Spatial
        self.spatial_count = np.zeros((0, 0, 0))
        self.spatial_density_count = np.zeros((0, 0, 0))
        self.spatial_density_rate = np.zeros((0, 0, 0))

        # Declustering
        self.valid_points_pre_decluster = []
        self.declustering_indices = {}
        self.other_data = {}
        self._previous_decluster_attributes = {}

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_all()

        # Figures
        fig_size = (5, 3)
        if _frontend == 'strive':
            fig_size = (90, 40)

        self.figure = {}
        if ('no_figures' not in kwargs):
            self.figures = {
                'map_view_catalog': {
                    'position': [0, 0],
                    'size': fig_size,
                    '3D_option': True,
                    'target': 'catalog_map_view'
                },
                'magnitude_distribution': {
                    'position': [0, 1],
                    'size': fig_size,
                    'target': 'catalog_magnitude_distribution'
                },
                'time_series': {
                    'position': [1, 0],
                    'size': fig_size,
                    'target': 'catalog_time_series'
                },
                'b_value_time': {
                    'position': [1, 1],
                    'size': fig_size,
                    'target': 'catalog_b_value_time'
                }
            }

        # Add gui elements
        self.gui_elements['catalog_source'] = {
            'element_type': 'entry',
            'command': 'file',
            'label': 'Catalog Path',
            'position': [0, 0],
            'filetypes': [('hdf5', '*.hdf5'), ('txt', '*.txt'), ('csv', '*.csv'), ('dat', '*.dat'), ('all', '*')]
        }

        self.gui_elements['use_comcat'] = {'element_type': 'check', 'label': 'Use ComCat', 'position': [1, 0]}

        self.gui_elements['comcat_min_magnitude'] = {
            'element_type': 'entry',
            'label': 'Min Magnitude Request',
            'position': [2, 0]
        }

        self.gui_elements['smoothing_kernal_sigma'] = {
            'element_type': 'entry',
            'label': 'Smoothing sigma',
            'position': [3, 0]
        }

        # Declustering GUI elements
        self.gui_elements['decluster_algorithms'] = {
            'element_type': 'checkbox',
            'position': [0, 1],
            'ncol': 1,
            'header': 'Declustering Algorithms:'
        }
        self.gui_elements['decluster_d'] = {
            'element_type': 'entry',
            'label': 'Fractal dimension (NN)',
            'position': [4, 1]
        }
        self.gui_elements['decluster_rfact'] = {
            'element_type': 'entry',
            'label': 'Number of crack radii (RS)',
            'position': [5, 1]
        }
        self.gui_elements['decluster_xk'] = {
            'element_type': 'entry',
            'label': 'Magnitude scaling factor (RS)',
            'position': [6, 1]
        }
        self.gui_elements['decluster_tau_min'] = {
            'element_type': 'entry',
            'label': 'Minimum look ahead time (RS)',
            'units': '(day)',
            'position': [7, 1]
        }
        self.gui_elements['decluster_tau_max'] = {
            'element_type': 'entry',
            'label': 'Maximum look ahead time (RS)',
            'units': '(day)',
            'position': [8, 1]
        }
        self.gui_elements['decluster_p'] = {
            'element_type': 'entry',
            'label': 'Confidence level (RS)',
            'position': [9, 1]
        }
        self.gui_elements['current_b_value_method'] = {
            'element_type': 'dropdown',
            'label': 'b-value method',
            'position': [10, 1],
            'values': list(self.b_value_methods.keys())
        }

    def __len__(self):
        """Return the length of catalog"""
        return len(self.epoch)

    def __bool__(self):
        """
        Quick test to see if data is loaded

        Returns:
            bool: Flag to indicate whether data is loaded

        """
        return self.__len__() > 0

    def __getitem__(self, islice):
        """Return a sliced copy of the catalog"""
        if isinstance(islice, slice):
            tmp = np.arange(len(self))
            islice = tmp[islice]

        elif np.ndim(islice) == 0:
            islice = np.array([islice])

        elif np.ndim(islice) > 1:
            raise ValueError()

        # Sort by epoch
        idx = np.argsort(self.epoch[islice])
        islice = islice[idx]

        sliced_catalog = SeismicCatalog(no_figures=True)
        sliced_catalog.latitude = self.latitude[islice]
        sliced_catalog.longitude = self.longitude[islice]
        sliced_catalog.depth = self.depth[islice]
        sliced_catalog.easting = self.easting[islice]
        sliced_catalog.northing = self.northing[islice]
        sliced_catalog.epoch = self.epoch[islice]
        sliced_catalog.magnitude = self.magnitude[islice]
        sliced_catalog.utm_zone = self.utm_zone
        sliced_catalog.t_origin = self.t_origin
        sliced_catalog.catalog_source = f"{self.catalog_source}_slice"
        sliced_catalog.old_catalog_source = sliced_catalog.catalog_source
        sliced_catalog.reset_slice()

        if self.declustering_indices:
            sliced_catalog.declustering_indices = {
                k: np.intersect1d(v, islice, assume_unique=True)
                for k, v in self.declustering_indices.items()
            }

        return sliced_catalog

    def __copy__(self):
        """Return a copy of the catalog"""
        new_catalog = SeismicCatalog(no_figures=True)
        new_catalog.latitude = self.latitude.copy()
        new_catalog.longitude = self.longitude.copy()
        new_catalog.depth = self.depth.copy()
        new_catalog.easting = self.easting.copy()
        new_catalog.northing = self.northing.copy()
        new_catalog.epoch = self.epoch.copy()
        new_catalog.magnitude = self.magnitude.copy()
        new_catalog.utm_zone = self.utm_zone
        new_catalog.t_origin = self.t_origin
        new_catalog.catalog_source = self.catalog_source
        new_catalog.old_catalog_source = new_catalog.catalog_source
        new_catalog.reset_slice()
        new_catalog.other_data = self.other_data.copy()

        return new_catalog

    def copy(self):
        """Return a copy of the catalog"""
        return self.__copy__()

    def set_origin(self, grid):
        """Set origin time"""
        self.t_origin = grid.t_origin

    def clear_data(self):
        """Clear catalog"""
        self.old_catalog_source = ''
        self.comcat_utm_zone = -100
        self.comcat_start_time = 0
        self.comcat_end_time = 0
        self.comcat_min_magnitude = 0
        self.comcat_min_magnitude_old = -100
        self.comcat_min_latitude = 0
        self.comcat_max_latitude = 0
        self.comcat_min_longitude = 0
        self.comcat_max_longitude = 0
        self.comcat_request_complete = False
        self.latitude = np.zeros(0)
        self.longitude = np.zeros(0)
        self.depth = np.zeros(0)
        self.easting = np.zeros(0)
        self.northing = np.zeros(0)
        self.epoch = np.zeros(0)
        self.magnitude = np.zeros(0)
        self.declustering_indices = {}
        self.data_slice = []

    def load_data(self, grid):
        """
        Load the seismic catalog if necessary
        """
        if self.catalog_source:
            if (self.catalog_source != self.old_catalog_source):
                f = os.path.expanduser(self.catalog_source)

                if not os.path.isfile(f):
                    self.clear_data()
                    return

                ext = os.path.splitext(f)[-1]

                try:
                    self._loader_map[ext](f)

                except KeyError:
                    self.logger.error(f"Unrecognized catalog type: {f}")

                self.old_catalog_source = self.catalog_source

        elif self.use_comcat:
            self.old_catalog_source = ''
            if grid.utm_zone:
                corner_a, corner_b = grid.get_lat_lon_box()
                epsilon = 1e-8
                time_epsilon = 60.0
                test = [
                    grid.utm_zone != self.comcat_utm_zone,
                    abs(corner_a[1] - self.comcat_min_latitude) > epsilon,
                    abs(corner_a[0] - self.comcat_min_longitude) > epsilon,
                    abs(corner_b[1] - self.comcat_max_latitude) > epsilon,
                    abs(corner_b[0] - self.comcat_max_longitude) > epsilon,
                    abs(self.comcat_min_magnitude - self.comcat_min_magnitude_old) > epsilon,
                    abs(grid.t_min + grid.t_origin - self.comcat_start_time) > time_epsilon,
                    abs(grid.t_max + grid.t_origin - self.comcat_end_time) > time_epsilon
                ]

                if any(test):
                    self.comcat_utm_zone = grid.utm_zone
                    self.comcat_min_latitude = corner_a[1]
                    self.comcat_min_longitude = corner_a[0]
                    self.comcat_max_latitude = corner_b[1]
                    self.comcat_max_longitude = corner_b[0]
                    self.comcat_min_magnitude_old = self.comcat_min_magnitude
                    self.comcat_start_time = grid.t_min + grid.t_origin
                    self.comcat_end_time = grid.t_max + grid.t_origin
                    self.load_comcat_catalog()

            else:
                self.logger.warning('UTM zone information not found in orion grid')

        if (grid.utm_zone != self.utm_zone):
            self.logger.debug(
                f"There is an apparent mismatch between the grid ({grid.utm_zone}) and catalog ({self.utm_zone}) utm zones"
            )

        self.set_origin(grid)
        self.check_declustering_requests()
        self.calculate_spatial_parameters(grid)

    def check_declustering_requests(self):
        """
        Check whether declustering parameters have changed
        and apply them if necessary
        """
        decluster_attributes = {
            "algorithms": self.decluster_algorithms,
            "d": self.decluster_d,
            "rfact": self.decluster_rfact,
            "xk": self.decluster_xk,
            "tau_min": self.decluster_tau_min,
            "tau_max": self.decluster_tau_max,
            "p": self.decluster_p,
        }

        # Always attempt to apply declustering when the catalog has been loaded/changed
        # Otherwise, re-apply declustering if any parameters have changed
        cond = True
        if self._previous_decluster_attributes:
            for k, v in decluster_attributes.items():
                vref = self._previous_decluster_attributes[k]
                cond = not (v == vref if k == "algorithms" else np.allclose(v, vref))
                if cond:
                    break

        self._previous_decluster_attributes.update(decluster_attributes)

        # Decluster the full catalog
        if cond:
            if not self.declustering_indices:
                self.declustering_indices = {"full": np.arange(self.N)}

            for algorithm, enabled in self.decluster_algorithms.items():
                if not enabled:
                    continue

                kwargs = {
                    k: decluster_attributes[k] if k in decluster_attributes else v
                    for k, v in decluster_kwargs[algorithm].items()
                }

                self.declustering_indices[algorithm] = self.decluster(algorithm, return_indices=True, **kwargs)

    def load_catalog_dict(self, data):
        """
        Load the seismic catalog from a dictionary.

        Required entries in the catalog include: epoch, magnitude, depth
        Location entries can include one of the following:
        * latitude, longitude
        * easting, northing (local coordinates)
        * easting, northing, utm_zone

        Args:
            data (dict): catalog dictionary
        """
        # Sort values by epoch
        Ia = np.argsort(data['epoch'])

        self.epoch = data['epoch'][Ia]
        self.magnitude = data['magnitude'][Ia]
        self.depth = data['depth'][Ia]

        # Load location information
        self.longitude = np.zeros(0)
        self.latitude = np.zeros(0)
        self.easting = np.zeros(0)
        self.northing = np.zeros(0)

        if 'longitude' in data:
            self.longitude = data['longitude'][Ia]
            self.latitude = data['latitude'][Ia]

        if 'easting' in data:
            self.easting = data['easting'][Ia]
            self.northing = data['northing'][Ia]

        if 'utm_zone' in data:
            self.utm_zone = data['utm_zone']
        else:
            self.utm_zone = ''

        # Reset declustering parameters
        self.declustering_indices = {}
        self._previous_decluster_attributes = {}

        self.other_data = {}
        targets = ['magnitude', 'depth', 'longitude', 'latitude', 'easting', 'northing', 'utm_zone']
        for k in data:
            if k not in targets:
                if len(data[k]) == self.N:
                    self.other_data[k] = data[k][Ia]
                else:
                    # If lengths differ, do not sort
                    self.other_data[k] = data[k]

        self.convert_coordinates()
        self.reset_slice()

    def load_catalog_array(self, **xargs):
        """
        Initialize catalog from pre-loaded arrays.
        Required arguments include: epoch, magnitude, depth
        Location entries can include one of the following:
        * latitude, longitude
        * easting, northing (local coordinates)
        * easting, northing, utm_zone

        Additional arguments will be placed in the other_data dict

        Args:
            epoch (np.ndarray): 1D array of event time in epoch
            depth (np.ndarray): 1D array of event depths
            magnitude (np.ndarray): 1D array of event magnitudes
            longitude (np.ndarray): 1D array of event longitudes
            latitude (np.ndarray): 1D array of event latitudes
            easting (np.ndarray): 1D array of event eastings
            northing (np.ndarray): 1D array of event northings
            utm_zone (str): UTM zone string (e.g.: '4SU')
        """
        self.load_catalog_dict(xargs)

    def load_catalog_hdf5(self, filename):
        """
        Load the seismic catalog from an hdf5 format file.
        See load_catalog_dict for required entries

        Args:
            filename (str): catalog file name
        """
        self.logger.info(f"Loading catalog from hdf5 format file: {filename}")
        with hdf5_wrapper.hdf5_wrapper(filename) as data:
            self.load_catalog_dict(data.get_copy())

    def load_catalog_csv(self, filename):
        """
        Reads .csv format seismic catalog files
        The file should have an optional first line with the zone information "utm_zone, zone_id"
        and a line with variable names separated by commas
        See load_catalog_dict for required entries

        Args:
            filename (str): catalog file name

        """
        self.logger.info(f"Loading catalog from csv format file: {filename}")
        value_names = []
        utm_zone = ''
        header_size = 1
        with open(filename) as f:
            line = f.readline()[:-1]
            if ('utm_zone' in line):
                header_size += 1
                utm_zone = line.split(',')[1].strip()
                line = f.readline()[:-1]
            value_names = [x.strip() for x in line.split(',')]

        tmp = np.loadtxt(filename, delimiter=',', skiprows=header_size, unpack=True)
        data = {'utm_zone': utm_zone}
        for ii, k in enumerate(value_names):
            data[k] = tmp[ii]
        self.load_catalog_dict(data)

    def load_catalog_zmap(self, filename):
        """
        Reads zmap (.dat) format seismic catalog files

        Args:
            filename (str): catalog file name

        """
        # Check the file format
        self.logger.debug('Loading zmap-format seismic catalog data')
        if '.dat' not in filename:
            raise Exception('File format not recognized')

        # Load the data
        latitude, longitude, year, month, day, magnitude, depth, hour, minute, second = np.loadtxt(filename,
                                                                                                   unpack=True)
        epoch = timestamp_conversion.convert_time_arrays(year, month, day, hour, minute, second)
        self.load_catalog_array(latitude=latitude, longitude=longitude, magnitude=magnitude, depth=depth, epoch=epoch)

    def load_catalog_txt(self, filename):
        """
        Reads .txt format seismic catalog files (oklahoma catalog)

        Args:
            filename (str): catalog file name

        """
        # Load the data
        # Note: depth is expected in km
        self.logger.debug('Loading txt-format seismic catalog data')
        longitude, latitude, depth, magnitude, epoch, dec_year = np.loadtxt(filename, unpack=True, skiprows=1)
        self.load_catalog_array(latitude=latitude,
                                longitude=longitude,
                                magnitude=magnitude,
                                depth=depth * 1e3,
                                epoch=epoch)

    def load_comcat_catalog(self):
        if 'csep' not in optional_packages:
            self.logger.warning('The optional csep package was not found... skipping comcat catalog requests')
            return

        import csep
        self.logger.info('Attempting to load comcat catalog')
        ta = datetime.date.fromtimestamp(self.comcat_start_time)
        tb = datetime.date.fromtimestamp(self.comcat_end_time)
        try:
            catalog = csep.query_comcat(ta,
                                        tb,
                                        min_magnitude=self.comcat_min_magnitude,
                                        min_longitude=self.comcat_min_longitude,
                                        max_longitude=self.comcat_max_longitude,
                                        min_latitude=self.comcat_min_latitude,
                                        max_latitude=self.comcat_max_latitude,
                                        verbose=True)

            # Note: pycsep seems to return milliseconds for epoch and km for depth
            self.load_catalog_array(latitude=catalog.get_latitudes(),
                                    longitude=catalog.get_longitudes(),
                                    magnitude=catalog.get_magnitudes(),
                                    depth=catalog.get_depths() * 1e3,
                                    epoch=catalog.get_epoch_times() * 1e-3)
        except Exception as e:
            self.logger.error('Could not fetch comcat catalog')
            self.logger.error(e)

        self.comcat_request_complete = True
        self.logger.info('Done!')

    def get_catalog_as_dict(self):
        """
        Save key catalog entries to a dict

        Returns:
            dict: A dictionary of catalog data
        """
        data = self.other_data.copy()
        data['epoch'] = self.epoch_slice
        data['magnitude'] = self.magnitude_slice
        data['depth'] = self.depth_slice

        longitude = self.longitude_slice
        latitude = self.latitude_slice
        if len(longitude):
            data['longitude'] = longitude
            data['latitude'] = latitude

        easting = self.easting_slice
        northing = self.northing_slice
        if len(easting):
            data['easting'] = easting
            data['northing'] = northing

        if self.utm_zone:
            data['utm_zone'] = self.utm_zone

        return data

    def save_catalog_hdf5(self, filename):
        """
        Save the seismic catalog to an hdf5 format file

        Args:
            filename (str): catalog file name
        """
        self.logger.info(f'Saving catalog to hdf5 format file: {filename}')
        catalog = self.get_catalog_as_dict()
        with hdf5_wrapper.hdf5_wrapper(filename, mode='w') as data:
            for k, value in catalog.items():
                data[k] = value

    def save_catalog_csv(self, filename):
        """
        Save the seismic catalog as a .csv format file

        Args:
            filename (str): catalog file name

        """
        self.logger.info(f'Saving catalog to csv format file: {filename}')
        catalog = self.get_catalog_as_dict()

        # Build the header
        header = ''
        if 'utm_zone' in catalog:
            header += f"utm_zone,{catalog['utm_zone']}\n"
            del catalog['utm_zone']
        header_keys = sorted(catalog.keys())
        header += ','.join(header_keys)

        # Split any tensor data
        initial_catalog_keys = list(catalog)
        for k in initial_catalog_keys:
            if isinstance(catalog[k], np.ndarray):
                M = np.shape(catalog[k])
                if (len(M) > 1):
                    tmp = np.reshape(catalog[k], (M[0], -1))
                    for ii in range(np.shape(tmp)[1]):
                        catalog[f"{k}_{ii}"] = np.squeeze(tmp[:, ii])
                    del catalog[k]

        # Assemble the data, padding where necessary to keep a consistent length
        N = max([len(catalog[k]) for k in catalog])
        for k in catalog:
            M = len(catalog[k])
            if M < N:
                catalog[k] = np.resize(catalog[k], N)

        # Save the data
        data = np.concatenate([np.expand_dims(catalog[k], -1) for k in header_keys], axis=1)
        np.savetxt(filename, data, delimiter=',', comments='', header=header)

    def convert_coordinates(self):
        """
        Convert utm coordinates to lat/lon or vice-versa if required
        """
        if len(self.longitude):
            if (len(self.easting) == 0):
                self.calculate_utm_coordinates()

        else:
            if self.utm_zone:
                self.calculate_latlon_coordinates()

    def calculate_utm_coordinates(self):
        """
        Convert catalog lat/lon coordinates to UTM
        """
        if self.N:
            tmp = utm.from_latlon(self.latitude, self.longitude)
            self.easting = tmp[0]
            self.northing = tmp[1]
            self.utm_zone = str(tmp[2]) + tmp[3]
        else:
            self.easting = np.zeros(0)
            self.northing = np.zeros(0)
            self.utm_zone = '1N'

    def calculate_latlon_coordinates(self):
        """
        Convert catalog UTM coordinates to lat/lon
        """
        if self.N:
            zone_id = int(self.utm_zone[:-1])
            zone_letter = self.utm_zone[-1]
            try:
                self.latitude, self.longitude = utm.to_latlon(self.easting, self.northing, zone_id, zone_letter)
            except utm.error.OutOfRangeError:
                self.logger.error('Unable to convert utm to lat/lon coordinates')
        else:
            self.latitude = np.zeros(0)
            self.longitude = np.zeros(0)

    def calculate_magnitude_rate(self, time_bins):
        """
        Estimate magnitude rate as a function of time

        Args:
            time_bins (list): bin values in time

        Returns:
            tuple: The bin centers, estimated magnitude rate in each bin
        """
        self.logger.debug('Calculating catalog moment rate')

        # Get data slices
        t_slice = self.relative_time
        magnitude_slice = self.magnitude_slice

        bin_centers = np.zeros(0)
        bin_magnitude_rate = np.zeros(0)

        if len(t_slice):
            # Find bins
            bin_ids = np.digitize(t_slice, time_bins) - 1
            dt = time_bins[1] - time_bins[0]
            bin_centers = time_bins[:-1] + 0.5 * dt
            bin_ids[bin_ids == len(bin_centers)] -= 1

            # Bin magnitude rate values
            bin_magnitude_rate = np.zeros(len(bin_centers))
            magnitude_rate_slice = (10.0**(1.5 * (magnitude_slice + 6))) / dt
            for catalog_index, time_index in enumerate(bin_ids):
                bin_magnitude_rate[time_index] += magnitude_rate_slice[catalog_index]

        return bin_centers, bin_magnitude_rate

    def calculate_cumulative_event_count(self, time_bins):
        """
        Count the number of events over time

        Args:
            time_bins (list): bin values in time

        Returns:
            tuple: The bin centers, event count in each bin
        """
        self.logger.debug('Calculating catalog cumulative event count')

        # Get data slices
        t_slice = self.relative_time
        bin_centers = np.zeros(0)
        bin_event_count = np.zeros(0)
        if len(t_slice):
            # bin_centers = 0.5 * (time_bins[:-1] + time_bins[1:])
            # bin_event_count = np.histogram(t_slice, time_bins)[0]
            tmp = np.cumsum(np.histogram(t_slice, time_bins)[0])
            bin_centers = time_bins.copy()
            bin_event_count = np.concatenate([tmp[:1], tmp], axis=0)

        return bin_centers, bin_event_count

    def calculate_seismic_characteristics(
        self,
        magnitude_bin_res=0.1,
        time_segments=10,
    ):
        """
        Generate various seismic characteristics

        Args:
            magnitude_bin_res (float): bin spacing for calculating a, b values
            time_segments (int): number of segments to calculate b values over time

        """
        self.logger.debug('Calculating catalog seismic characteristics')

        # Get the slice data
        magnitude_slice = self.magnitude_slice
        t_slice = self.relative_time

        if len(t_slice):
            # Determine the global a, b values
            self.a_value, self.b_value = self.estimate_a_b_value(magnitude_slice)
            if len(magnitude_slice) >= self.b_value_min_points:
                self.magnitude_completeness = mbs(magnitude_slice, mbin=0.1)[0]
            else:
                self.magnitude_completeness = 0.0
            self.magnitude_bins = np.arange(np.min(magnitude_slice), np.max(magnitude_slice) + 1, 0.1)
            self.cumulative_frequency = np.histogram(magnitude_slice, self.magnitude_bins)[0]

            # Calculate the b-value as a function of time
            self.varying_b_value = np.zeros(time_segments)
            t_bins = np.linspace(np.amin(t_slice) - 60.0, np.amax(t_slice) + 60.0, time_segments + 1)
            self.varying_b_time = t_bins[:-1] + 0.5 * (t_bins[1] - t_bins[0])
            bin_ids = np.digitize(t_slice, t_bins) - 1
            for ii in range(time_segments):
                Isplit = np.where(bin_ids == ii)
                self.varying_b_value[ii] = self.estimate_a_b_value(magnitude_slice[Isplit])[1]

            # Estimate magnitude rate as a function of time
            time_bins = np.linspace(self.time_range[0], self.time_range[-1], self.magnitude_rate_resolution + 1)
            self.magnitude_rate_time, self.magnitude_rate = self.calculate_magnitude_rate(time_bins)
        else:
            self.a_value = 0.0
            self.b_value = 0.0
            self.magnitude_completeness = -1.0
            self.magnitude_bins = np.linspace(-3.0, 3.0, 7)
            self.cumulative_frequency = np.zeros(7)
            self.varying_b_value = np.zeros(0)
            self.varying_b_time = np.zeros(0)
            self.magnitude_rate_time = np.zeros(0)
            self.magnitude_rate = np.zeros(0)

        self.logger.debug(f"Estimated magnitude of completeness = {self.magnitude_completeness:1.2f}")

    def reset_slice(self):
        """
        Set the catalog time slice to fit the entire catalog
        """
        self.time_range = [-1e99, 1e99]
        self.magnitude_range = [-1e99, 1e99]
        self.data_slice = np.arange(self.N)
        self.type = "full"

        if self.N:
            self.calculate_seismic_characteristics()

    def set_slice(
        self,
        time_range=None,
        magnitude_range=None,
        minimum_interevent_time=0.0,
        type_=None,
        inplace=True,
    ):
        """
        Set the catalog time slice

        Args:
            time_range (list): list of sub-catalog min/max times
            magnitude_range (list): list of sub-catalog min/max event magnitudes
            minimum_interevent_time (float): only include events if this amount of time has elapsed since the last
            type_ (str): catalog type
            inplace (bool): if True, set slice in-place
        """
        self.logger.debug('Setting seismic catalog slice')

        time_range = time_range if time_range is not None else [-1e99, 1e99]
        magnitude_range = magnitude_range if magnitude_range is not None else [-1e99, 1e99]
        type_ = type_ if type_ is not None else self.type

        if inplace:
            self.time_range = time_range
            self.magnitude_range = magnitude_range

        t = self.epoch - self.t_origin
        valid_points = np.ones(self.N, dtype=bool)

        if time_range[0] > -1e98:
            self.logger.debug(f"t_min={time_range[0]:1.1f} s")
            valid_points[t < time_range[0]] = False

        if time_range[1] < 1e98:
            self.logger.debug(f"t_max={time_range[1]:1.1f} s")
            valid_points[t > time_range[1]] = False

        if magnitude_range[0] > -1e98:
            self.logger.debug(f"m_min={magnitude_range[0]:1.1f}")
            valid_points[self.magnitude < magnitude_range[0]] = False

        if magnitude_range[1] < 1e98:
            self.logger.debug(f"m_max={magnitude_range[1]:1.1f}")
            valid_points[self.magnitude > magnitude_range[1]] = False

        if minimum_interevent_time > 0.0:
            last_t = -1e99

            for i, (ti, valid_point) in enumerate(zip(t, valid_points)):
                if valid_point:
                    if ti - last_t < minimum_interevent_time:
                        valid_points[i] = False

                    else:
                        last_t = ti

        self.valid_points_pre_decluster = valid_points
        return self.finalize_slice(type_, inplace)

    def finalize_slice(self, type_=None, inplace=True):
        """
        Apply the declustering method and finalize the catalog realization

        Args:
            type_ (str): catalog type
            inplace (bool): if True, set slice in-place
        """
        valid_points = self.valid_points_pre_decluster.copy()
        if self.declustering_indices and (type_ is not None):
            valid_points = np.intersect1d(
                np.flatnonzero(valid_points),
                self.declustering_indices[type_],
                assume_unique=True,
            )

        if inplace:
            self.data_slice = valid_points
            target = self

        else:
            target = self[valid_points]

        if len(valid_points):
            target.calculate_seismic_characteristics()

        if type_ not in self.declustering_indices:
            # self.logger.error(f"Unknown catalog type '{type_}'")
            target.type = self.type

        else:
            target.type = type_

        if not inplace:
            return target

    def save_csep_ascii_format(self, fname):
        self.logger.info('Exporting catalog in csep ascii format...')
        with open(os.path.expanduser(fname), 'w') as f:
            f.write('lon,lat,mag,time_string,depth,catalog_id,event_id\n')
            latitude = self.latitude_slice
            longitude = self.longitude_slice
            depth = self.depth_slice
            epoch = self.epoch_slice
            magnitude = self.magnitude_slice
            for i, (lat, lon, mag, t, z) in enumerate(zip(latitude, longitude, magnitude, epoch, depth)):
                f.write(f"{lat},{lon},{mag},{timestamp_conversion.get_time_str_pycsep(t)},{z * 1e-3},orion,{i:06d}\n")
        self.logger.debug('Finished writing catalog')

    def get_plot_location(self, grid):
        if (grid.spatial_type == 'UTM'):
            x = self.easting_slice - grid.x_origin
            y = self.northing_slice - grid.y_origin

        else:
            x = self.longitude_slice
            y = self.latitude_slice

        z = self.depth_slice - grid.z_origin
        return x, y, z

    def get_scaled_point_size(self, x, point_scale=0.5):
        x_range = [0.0, 1.0]
        N = len(x)
        if N > 0:
            x_range = [np.amin(x), np.amax(x)]
        point_size = point_scale * (3**(1 + x - x_range[0]))
        return point_size

    def calculate_spatial_parameters(self, grid):
        count_xyzt = grid.histogram_values(self.easting_slice,
                                           self.northing_slice,
                                           self.depth_slice,
                                           self.relative_time,
                                           include_edges=True)
        count_txy = np.sum(np.moveaxis(count_xyzt, -1, 0), axis=3)

        # smooth_kernel = np.ones((3, 1, 1))
        # smooth_kernel /= np.sum(smooth_kernel)
        # count_txy = ndimage.convolve(count_txy, smooth_kernel)
        k = 1.0
        if ',' in self.smoothing_kernal_sigma:
            k = tuple([float(x) for x in self.smoothing_kernal_sigma.split(',')])
        else:
            k = float(self.smoothing_kernal_sigma)
        count_txy = ndimage.gaussian_filter(count_txy, k)

        self.spatial_count = np.cumsum(count_txy, axis=0)
        self.spatial_density_count = self.spatial_count / np.expand_dims(grid.areas, 0)
        self.spatial_density_rate = other.derivative(self.spatial_density_count, grid.t, axis=0)

    def get_plot_data(self, projection):
        self.reset_slice()
        t_scale = 60 * 60 * 24.0
        catalog_ne_t, catalog_ne = self.calculate_cumulative_event_count(projection.t)
        return {
            'x': self.easting_slice - projection.x_origin,
            'y': self.northing_slice - projection.y_origin,
            'z': self.depth_slice - projection.z_origin,
            'latitude': self.latitude_slice,
            'longitude': self.longitude_slice,
            'time': self.relative_time / t_scale,
            'magnitude': self.magnitude_slice,
            'point_size': self.scaled_point_size_slice,
            'catalog_cumulative_event_count_t': catalog_ne_t,
            'catalog_cumulative_event_count': catalog_ne
        }

    def update_plot_data(self, **kwargs):
        self.logger.debug('Generating seismic catalog plots')
        self.reset_slice()
        self._plot_data = {}
        if self.N:
            grid = kwargs.get('GridManager')
            self._plot_data['seismic_locations'] = self.get_plot_location(grid)

    def catalog_map_view(self, plot_data):
        tmp = plot_data['Seismic Catalog']
        layers = {
            'ms': {
                'x': tmp['x'],
                'y': tmp['y'],
                'c': tmp['time'],
                's': tmp['point_size'],
                't': {
                    'Magnitude': tmp['magnitude']
                },
                'type': 'scatter'
            }
        }
        axes = {'x': 'X (m)', 'y': 'Y (m)', 'c': 'Time (days)', 's': 'Marker'}
        return layers, axes

    def catalog_magnitude_distribution(self, plot_data):
        count = 10**(self.a_value - self.b_value * self.magnitude_bins)
        bins = self.magnitude_bins
        bin_height = self.cumulative_frequency

        layers = {
            'gutenberg_richter_ab': {
                'x': bins,
                'y': count,
                'type': 'line'
            },
            'magnitude_distribution': {
                'x': bins,
                'y': bin_height,
                'type': 'bar'
            }
        }
        axes = {'x': 'Magnitude', 'y': 'Count', 'log_y': True}
        return layers, axes

    def catalog_time_series(self, plot_data):
        t_scale = 60 * 60 * 24.0
        t = self.relative_time / t_scale
        magnitude = self.magnitude_slice
        x, y, z = self._plot_data.get('seismic_locations', [np.zeros(0), np.zeros(0), np.zeros(0)])

        layers = {'ms': {'x': t, 'y': magnitude, 'c': z, 'type': 'scatter'}}
        axes = {'x': 'Time (days)', 'y': 'Magnitude', 'c': 'Depth (m)'}
        return layers, axes

    def catalog_b_value_time(self, plot_data):
        t_scale = 60 * 60 * 24.0
        t = self.varying_b_time / t_scale
        b = self.varying_b_value

        layers = {'ms': {'x': t, 'y': b, 'type': 'line'}}
        axes = {'x': 'Time (days)', 'y': 'b-value'}
        return layers, axes

    def generate_plots(self, **kwargs):
        self.logger.debug('Generating seismic catalog plots')
        self.reset_slice()
        grid = kwargs.get('grid')
        appearance = kwargs.get('appearance')

        # Set plot data
        if self.N:
            magnitude = self.magnitude_slice
            t_scale = 60 * 60 * 24.0
            t = self.relative_time / t_scale
            M = len(magnitude)
            magnitude_range = [0.0, 1.0]
            if M > 0:
                magnitude_range = [np.amin(magnitude), np.amax(magnitude)]
            ms_point_size = self.scaled_point_size_slice

            # Map/3D view
            x_range, y_range = grid.get_plot_range()
            x, y, z = self.get_plot_location(grid)

            ax = self.figures['map_view_catalog']['handle'].axes[0]
            ax.cla()
            ax.xaxis.set_major_locator(MaxNLocator(5))
            ax.yaxis.set_major_locator(MaxNLocator(5))
            ca = None
            if appearance.active_plot_types == '2D':
                ca = ax.scatter(x,
                                y,
                                s=ms_point_size,
                                c=t,
                                cmap=gui_colors.point_colormap,
                                edgecolors='k',
                                linewidths=0.1)
            else:
                ax.zaxis.set_major_locator(MaxNLocator(5))
                ca = ax.scatter(x,
                                y,
                                z,
                                s=ms_point_size,
                                c=t,
                                cmap=gui_colors.point_colormap,
                                edgecolors='k',
                                linewidths=0.1)
            ax.set_xlim(x_range)
            ax.set_ylim(y_range)
            if 'colorbar' not in self.figures['map_view_catalog']:
                self.figures['map_view_catalog']['colorbar'] = self.figures['map_view_catalog']['handle'].colorbar(
                    ca, ax=ax)
                self.figures['map_view_catalog']['colorbar'].set_label('t (days)')
            self.figures['map_view_catalog']['colorbar'].update_normal(ca)

            # Magnitude distribution
            tmp_N = 10**(self.a_value - self.b_value * self.magnitude_bins)
            tmp_w = self.magnitude_bins[1] - self.magnitude_bins[0]
            # complete_N = 1.5 * 10**(self.a_value - self.b_value * self.magnitude_completeness)

            ax = self.figures['magnitude_distribution']['handle'].axes[0]
            ax.cla()
            ax.bar(self.magnitude_bins[:-1], self.cumulative_frequency, tmp_w, **gui_colors.histogram_style)
            ax.semilogy(self.magnitude_bins,
                        tmp_N,
                        label=f"a={self.a_value:1.2f}, b={self.b_value:1.2f}",
                        **gui_colors.alt_line_style)
            ax.legend(loc=1)

            # Time series
            ax = self.figures['time_series']['handle'].axes[0]
            ax.cla()
            if M > 0:
                sh = ax.stem(t,
                             magnitude,
                             linefmt=gui_colors.line_style['color'],
                             markerfmt='None',
                             use_line_collection=True,
                             bottom=np.floor(np.amin(magnitude)))
                plt.setp(sh[1], linewidth=0.5)
                ax.plot(t, magnitude, **gui_colors.point_style, markersize=3)
            if grid.plot_time_min < grid.plot_time_max:
                ax.set_xlim(grid.plot_time_min, grid.plot_time_max)
            else:
                ax.set_xlim(grid.t_min / t_scale, grid.t_max / t_scale)
            ax.set_ylim(magnitude_range)

            # B value with time
            ax = self.figures['b_value_time']['handle'].axes[0]
            ax.cla()
            ax.plot(self.varying_b_time / t_scale, self.varying_b_value, **gui_colors.line_style)
            if grid.plot_time_min < grid.plot_time_max:
                ax.set_xlim(grid.plot_time_min, grid.plot_time_max)
            else:
                ax.set_xlim(grid.t_min / t_scale, grid.t_max / t_scale)

        # Setup figure axes labels, titles
        ax = self.figures['map_view_catalog']['handle'].axes[0]
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
        ax.set_title('Map View')

        ax = self.figures['magnitude_distribution']['handle'].axes[0]
        ax.set_xlabel('Magnitude')
        ax.set_ylabel('N')
        ax.set_title('Magnitude Distribution')

        ax = self.figures['time_series']['handle'].axes[0]
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('magnitude')
        ax.set_title('Time Series')

        ax = self.figures['b_value_time']['handle'].axes[0]
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('b-value')
        ax.set_title('b-value Variations')

    def decluster(self, algorithm, return_indices=False, **kwargs):
        """
        Decluster catalog.

        Args:
            algorithm (str): declustering algorithm {'gardner-knopoff', 'nearest-neighbor', 'reasenberg'}
            return_indices (bool): if True, returns indices of background events instead of declustered catalog

        """
        import bruces

        if algorithm == "nearest-neighbor" and "w" not in kwargs:
            kwargs["w"] = self.b_value

        # Filter out events with magnitude lower than Mc
        imc = np.flatnonzero(self.magnitude > self.magnitude_completeness)

        self.logger.info(f"Declustering catalog using algorithm '{algorithm}'")
        cat = bruces.Catalog(
            origin_times=self.epoch[imc].astype("datetime64[ms]"),
            eastings=self.easting[imc],
            northings=self.northing[imc],
            depths=self.depth[imc] * 1.0e-3,
            magnitudes=self.magnitude[imc],
        )
        idx = cat.decluster(algorithm, return_indices=True, **kwargs)
        idx = imc[idx]

        return idx if return_indices else self[idx]

    def decluster_realizations(self, inplace=True):
        """
        Iterate over all declustering realizations for the current slice

        Args:
            inplace (bool): if True, set slice in-place
        """
        return DeclusterMethodIterator(self, inplace)

    def estimate_a_b_value(self, magnitudes):
        """
        Estimate the Gutenberg Richter a, b values

        Args:
            magnitudes (np.ndarray): Magnitude values

        Returns:
            tuple: a, b value
        """
        N = len(magnitudes)
        if N < self.b_value_min_points:
            self.logger.warning(
                f'b-value calculations require a minimum of {self.b_value_min_points} events (actual={N})')
            return self.a_value_default, self.b_value_default

        if self.current_b_value_method not in self.b_value_methods:
            self.logger.warning(f'Requested b-value method was not found: {self.current_b_value_method}')
            return self.a_value_default, self.b_value_default

        try:
            # TODO: Estimate the a-value from the data
            b = self.b_value_methods[self.current_b_value_method](magnitudes)
            return self.a_value_default, b
        except Exception as e:
            print(e)
            self.logger.error('b-value calculation resulted in an exception')
            return self.a_value_default, self.b_value_default

    @property
    def N(self):
        """Length of the catalog"""
        return len(self)

    @property
    def latitude_slice(self):
        """
        Get the catalog latitude slice
        """
        return self.latitude[self.data_slice]

    @property
    def longitude_slice(self):
        """
        Get the catalog longitude slice
        """
        return self.longitude[self.data_slice]

    @property
    def depth_slice(self):
        """
        Get the catalog depth slice
        """
        return self.depth[self.data_slice]

    @property
    def easting_slice(self):
        """
        Get the catalog easting slice
        """
        return self.easting[self.data_slice]

    @property
    def northing_slice(self):
        """
        Get the catalog northing slice
        """
        return self.northing[self.data_slice]

    @property
    def epoch_slice(self):
        """
        Get the catalog time slice
        """
        return self.epoch[self.data_slice]

    @property
    def relative_time(self):
        """
        Get the catalog relative time
        """
        return self.epoch_slice - self.t_origin

    @property
    def magnitude_slice(self):
        """
        Get the catalog magnitude slice
        """
        return self.magnitude[self.data_slice]

    @property
    def scaled_point_size_slice(self):
        """
        Get the catalog magnitude slice
        """
        return self.get_scaled_point_size(self.magnitude_slice)

    @property
    def magnitude_rate_data_slice(self):
        """
        Get the estimated catalog magnitude rate, time vector
        """
        return self.magnitude_rate_time, self.magnitude_rate


def gutenberg_richter_b_positive(magnitudes):
    """
    Estimate the Gutenberg Richter b value using the b-positive method

    Args:
        magnitudes (np.ndarray): Magnitude values

    Returns:
        float: b value
    """
    differences = []

    for i in range(len(magnitudes[:-1])):
        diff = magnitudes[i + 1] - magnitudes[i]
        differences.append(diff)

    addINT = 0
    differences.insert(0, addINT)

    mdiff_pos = [x for x in differences if x > 0]
    delta_mag_mean = np.mean(mdiff_pos)
    minmagThreshold = 0.1

    # estimating the mle b-value
    tmp_b = np.log10(np.e) / (delta_mag_mean - minmagThreshold)

    return tmp_b


def fmd(magnitudes, mbin):
    """
    TODO: Add documentation for this function here and change the name of the function to something human readable
    Note: in this function, you had created a variable with the same name as the function...  That could lead to some bad unexpected behavior

    Args:
        magnitudes (np.ndarray): Magnitude values

    Returns:
        float: b value
    """
    Nmag = len(magnitudes)
    minmag = np.min(magnitudes)
    maxmag = np.max(magnitudes)
    m_bins = np.arange(minmag, maxmag + 0.8, mbin)    # 0.8 to extend best fit discrete/cumulative lines
    nbins = len(m_bins)
    dis_mf = np.zeros(nbins)
    cum_mf = np.zeros(nbins)
    for i in range(nbins):
        cum_mf[i] = np.sum(magnitudes > m_bins[i] - mbin / 2)
    dis_mf = np.absolute(np.diff(np.concatenate((cum_mf, [0]), axis=0)))
    Fmd = collections.namedtuple('Fmd', ['Nmag', 'm_bins', 'dis_mf', 'cum_mf'])
    return Fmd(Nmag, m_bins, dis_mf, cum_mf)


def maxc(magnitudes, mbin):
    """
    TODO: Add documentation for this function here and change the name of the function to something human readable

    Args:
        magnitudes (np.ndarray): Magnitude values

    Returns:
        float: b value
    """
    FMD = fmd(magnitudes, mbin)
    mc = FMD.m_bins[FMD.dis_mf == np.max(FMD.dis_mf)]
    return mc


def GR_mle(magnitudes, mco, mbin):
    """
    TODO: Add documentation for this function here and change the name of the function to something human readable

    Args:
        magnitudes (np.ndarray): Magnitude values

    Returns:
        tuple: b_mle, b_unc, a_mle
    """
    if len(magnitudes) < 2:
        return 1.0, 1.0, 1.0

    nbev = len(magnitudes)
    b_mle = np.log10(np.exp(1)) / (np.mean(magnitudes) - (mco - mbin / 2))
    b_unc = (2.3 * b_mle**2) * np.sqrt(np.sum((magnitudes - np.mean(magnitudes))**2) / (nbev * (nbev - 1)))
    a_mle = np.log10(nbev) + b_mle * mco

    return b_mle, b_unc, a_mle


def mbs(magnitudes, mbin):
    """
    TODO: Add documentation for this function here and change the name of the function to something human readable

    Args:
        magnitudes (np.ndarray): Magnitude values

    Returns:
        float: b value
    """
    maxmag = np.max(magnitudes)
    maxc_mc = maxc(magnitudes, mbin)
    maxc_mc = maxc_mc[0]
    Mco = maxc_mc + np.arange(-0.7, 3.0, mbin)
    n_bs = len(Mco)
    bi = np.zeros(n_bs)
    unc = np.zeros(n_bs)
    for i in range(n_bs):
        magnitudes_sel = magnitudes[magnitudes > Mco[i] - mbin / 2]
        n_magnitudes_sel = len(magnitudes_sel)
        GR_paras = GR_mle(magnitudes_sel, Mco[i], mbin)
        bi[i] = GR_paras[0]
        unc[i] = GR_paras[1]
    bave = np.zeros(n_bs - 5)
    for i in range(n_bs - 5):
        bave[i] = np.mean(bi[i:i + 5])
    dbi = np.abs(bave - bi[0:n_bs - 5])
    logic_dbi = dbi <= unc[0:n_bs - 5]
    Mco_sel = Mco[0:n_bs - 5][logic_dbi]
    if len(Mco_sel) == 0:
        Mc_mbs = maxc_mc
    else:
        Mc_mbs = Mco_sel[0]
    MBS = collections.namedtuple('MBS', ['Mc_mbs', 'Mco', 'bi', 'unc', 'bave'])
    mbs = MBS(Mc_mbs, Mco, bi, unc, bave)
    return mbs


def gutenberg_richter_b_mle(magnitudes):
    """
    Legacy least-squares method for estimating b-values.
    This method tends to return much smaller b-values than expected and should be avoided if possible.

    Args:
        magnitudes (ndarray): 1D array of magnitudes

    Returns:
        b-value (float)
        a-value (float)
    """
    tmp_mbs = mbs(magnitudes, mbin=0.1)
    mc = tmp_mbs[0]

    # estimating the mle b-value
    tmp_b = np.log10(np.e) / (np.mean(magnitudes) - mc + 0.05)
    # tmp_a = np.log10(len(magnitudes)) + tmp_b * (mc + 0.05)

    return tmp_b


class DeclusterMethodIterator():

    def __init__(self, catalog: SeismicCatalog, inplace: bool):
        self.catalog = catalog
        self.inplace = inplace
        self.decluster_ordered = sorted(catalog.declustering_indices.keys())
        if not self.decluster_ordered:
            self.decluster_ordered = [None]
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.decluster_ordered):
            decluster_method = self.decluster_ordered[self.n]
            self.catalog.finalize_slice(type_=decluster_method, inplace=self.inplace)
            self.n += 1
            if not decluster_method:
                decluster_method = 'full'
            return decluster_method, self.catalog

        else:
            raise StopIteration
