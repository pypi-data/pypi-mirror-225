# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
well_database.py
-----------------------
"""

import numpy as np
import orion
from orion.managers import manager_base
from orion.utilities import hdf5_wrapper, timestamp_conversion
from orion.utilities.plot_config import gui_colors
from orion.external_database import (california_doggr, oklahoma_corporation_commission, texas_railroad_commission)
from orion import _frontend
import os
import time
import shutil
from orion.managers.manager_base import block_thread, recursive


class WellDatabase(manager_base.ManagerBase):
    """
    A class for managing well database information

    Attributes:
        net_volume (np.ndarray): Cumulative fluid injection time series (at grid.t)
    """

    def set_class_options(self, **kwargs):
        """
        Well manager initialization
        """
        # Set the shorthand name
        self.short_name = 'Well Database'
        self.show_plots = True

        # Data sources
        self.database_path = os.path.join(self.cache_root, 'well_database')
        self.update_external_data_btn = 'Update data'
        self.clean_external_wells_btn = 'Clear data'
        self.autopick_external_wells_btn = 'Autopick wells'
        self.external_request_start = ''
        self.external_request_end = ''
        self.grid_buffer_time = 1.0
        self.time_request_start = 0.0
        self.time_request_end = 0.0

        self.external_datasets = {
            'OK_Corp_Commission': {
                'url': 'https://oklahoma.gov/occ/divisions/oil-gas/oil-gas-data.html'
            },
            'TX_Railroad_Commission': {
                'url': 'https://www.rrc.texas.gov/resource-center/research/research-queries/'
            },
            'CA_DOGGR_OilGas': {
                'url': 'https://filerequest.conservation.ca.gov/?q=production_injection_data'
            },
            'CA_DOGGR_Geothermal': {
                'url': 'https://www.conservation.ca.gov/calgem/geothermal/manual/Pages/production.aspx'
            }
        }

        self.available_sources = ['(none)'] + sorted(list(self.external_datasets.keys()))
        self.active_source = self.available_sources[0]

        # Etc
        self.last_well_list = []
        self.last_time_range = [0.0, 0.0]

    @recursive
    def process_inputs(self):
        """
        Check input values
        """
        if os.path.isfile(self.database_path):
            self.logger.warning('Well database path should target a directory... changing to the parent directory')
            self.database_path = os.path.dirname(self.database_path)

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.well_dataset = {}

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Figures
        fig_size = (7, 6)
        if _frontend == 'strive':
            fig_size = (90, 40)

        self.figures['spatial_well_database'] = {'position': [0, 0], 'size': fig_size, 'target': 'well_database_map'}

        # Gui elements
        # Note: these will point to the class members by name
        self.gui_elements = {}

        self.gui_elements['database_path'] = {
            'element_type': 'entry',
            'command': 'file',
            'label': 'Database Path',
            'position': [0, 0],
            'user': True,
            'filetypes': ['folder']
        }

        self.gui_elements['active_source'] = {
            'element_type': 'dropdown',
            'label': 'Data source',
            'position': [1, 0],
            'user': True,
            'values': self.available_sources,
            'columnspan': 3
        }

        self.gui_elements['external_request_start'] = {
            'element_type': 'entry',
            'label': 'Request Range',
            'position': [2, 0],
            'user': True,
        }

        self.gui_elements['external_request_end'] = {
            'element_type': 'entry',
            'position': [2, 1],
            'user': True,
            'units': timestamp_conversion.time_units,
            'units_span': 10
        }

        self.gui_elements['grid_buffer_time'] = {
            'element_type': 'entry',
            'position': [3, 0],
            'user': True,
            'label': 'Autopick Time Buffer',
            'units': '(years)',
            'units_span': 4
        }

        if _frontend == 'strive':
            return

        self.gui_elements['update_external_data_btn'] = {
            'element_type': 'button',
            'text': 'Update Database',
            'command': self.update_external_data,
            'position': [4, 0],
            'pre_update': 'all'
        }
        self.gui_elements['clean_external_wells_btn'] = {
            'element_type': 'button',
            'text': 'Cleanup Database',
            'command': self.clean_external_wells,
            'position': [4, 1]
        }
        self.gui_elements['autopick_external_wells_btn'] = {
            'element_type': 'button',
            'text': 'Autopick',
            'command': self.autopick_external_wells,
            'position': [4, 2],
            'target_arg_names': ['GridManager', 'WellManager'],
            'pre_update': 'all'
        }

    def set_dataset(self):
        if not self.database_path:
            self.well_dataset = {}
            return

        # Setup target directories
        dataset_root = os.path.abspath(self.database_path)
        os.makedirs(dataset_root, exist_ok=True)

        # Setup the database
        fname = os.path.join(dataset_root, 'well_dataset.hdf5')
        with hdf5_wrapper.hdf5_wrapper(fname, mode='w') as data:
            for ka in self.external_datasets.keys():
                # Setup external database metadata
                data[ka] = {'metadata': {'well_segment_ids': {}}}
                for kb in ['well_names', 'utm_zone', 'api']:
                    data[ka]['metadata'][kb] = np.empty(0, dtype=str)
                for kb in [
                        'latitude', 'longitude', 'depth', 'easting', 'northing', 'segment_start_time',
                        'segment_end_time'
                ]:
                    data[ka]['metadata'][kb] = np.empty(0, dtype=str)

                # Setup separate data holders
                child_file_path = os.path.join(dataset_root, f'{ka}.hdf5')
                with hdf5_wrapper.hdf5_wrapper(child_file_path, mode='w') as tmp:
                    tmp['segment_epoch'] = {}
                    tmp['wells'] = {}

                # Link to the primary database
                data[ka].link('data', child_file_path)

    @block_thread
    def load_data(self, *xargs):
        if not hasattr(self, 'well_dataset'):
            self.well_dataset = {}

        dataset_root = os.path.abspath(self.database_path)
        fname = os.path.join(dataset_root, 'well_dataset.hdf5')
        if not os.path.isfile(fname):
            self.set_dataset()

        if isinstance(self.well_dataset, hdf5_wrapper.hdf5_wrapper):
            return

        # Load the file and check it for errors
        self.well_dataset = hdf5_wrapper.hdf5_wrapper(fname)
        database_errors = 0
        required_keys = ['well_names', 'latitude', 'longitude', 'depth', 'api', 'utm_zone', 'easting', 'northing']
        for ka in self.external_datasets.keys():
            tkeys = list(self.well_dataset[ka]['metadata'].keys())
            for kb in required_keys:
                if kb not in tkeys:
                    self.logger.error(f"The well database is missing an expected key: {ka}/{kb}")
                    self.logger.error(f"Try deleting the well database located here: {self.database_path}")
                    database_errors += 1

        if database_errors:
            del self.well_dataset
            self.well_dataset = {}

    def update_external_data(self):
        # Check for database
        if (self.active_source not in self.well_dataset.keys()):
            return

        # Check range requests
        time_range = []
        if self.external_request_start:
            time_range.append(timestamp_conversion.convert_timestamp(self.external_request_start))
        else:
            time_range.append(0)

        if self.external_request_end:
            time_range.append(timestamp_conversion.convert_timestamp(self.external_request_end))
        else:
            time_range.append(time.time())

        # Find potential gaps in downloaded data
        data = self.well_dataset[self.active_source]
        metadata = data['metadata']
        time_requests = [time_range]
        ta = metadata['segment_start_time']
        tb = metadata['segment_end_time']
        for data_ta, data_tb in zip(ta, tb):
            new_requests = []
            for request_ta, request_tb in time_requests:
                # left, right, left-intersect, right-intersect
                if (request_tb <= data_ta):
                    new_requests.append([request_ta, request_tb])
                if (request_ta >= data_tb):
                    new_requests.append([request_ta, request_tb])
                if ((request_ta < data_ta) & (request_tb >= data_ta)):
                    new_requests.append([request_ta, data_ta])
                if ((request_ta <= data_tb) & (request_tb > data_tb)):
                    new_requests.append([data_tb, request_tb])
            time_requests = new_requests

        # Acquire segments
        segments_to_add = []
        for request in time_requests:
            ta = timestamp_conversion.get_time_string(request[0])
            tb = timestamp_conversion.get_time_string(request[1])
            self.logger.debug(f'Requesting well data from {self.active_source} in range: ({ta}, {tb})')

            new_segments = []
            try:
                if (self.active_source == 'OK_Corp_Commission'):
                    new_segments = oklahoma_corporation_commission.load_OK_Corp_Commission_data(*request)
                elif (self.active_source == 'TX_Railroad_Commission'):
                    new_segments = texas_railroad_commission.load_TX_Railroad_Commission_data(*request)
                elif (self.active_source == 'CA_DOGGR_OilGas'):
                    new_segments = california_doggr.load_CA_DOGGR_OilGas_data(*request)
                elif (self.active_source == 'CA_DOGGR_Geothermal'):
                    new_segments = california_doggr.load_CA_DOGGR_Geothermal_data(*request)
            except Exception as e:
                self.logger.error(e)

            if isinstance(new_segments, dict):
                new_segments = [new_segments]

            for s in new_segments:
                if ('epoch' in s.keys()):
                    if len(s['epoch']):
                        segments_to_add.append(s)

        self.add_data_segments(segments_to_add)

    def add_data_segments(self, segments_to_add):
        if not segments_to_add:
            return

        if self.active_source not in self.well_dataset.keys():
            return

        # Get a copy of the existing child database
        target = self.well_dataset[self.active_source].get_copy()
        metadata = target['metadata']
        data = target['data']

        for segment in segments_to_add:
            self.logger.debug('Adding segment to well data cache')

            # Record the segment information
            N = str(len(metadata['segment_start_time']))
            metadata['segment_start_time'] = np.append(metadata['segment_start_time'], segment['segment_range'][0])
            metadata['segment_end_time'] = np.append(metadata['segment_end_time'], segment['segment_range'][1])
            data['segment_epoch'][N] = segment['epoch']

            # Check for new wells
            new_wells = []
            initial_wells = list(metadata['well_names'])
            for ka, well_metadata in segment['metadata'].items():
                if ka not in initial_wells:
                    # Create a new well file
                    new_wells.append(ka)
                    data['wells'][ka] = {'pressure': {}, 'flow_rate': {}, 'metadata': well_metadata}
                    metadata['well_segment_ids'][ka] = np.empty(0, dtype=str)

                # Record the segment ID and data for the well
                metadata['well_segment_ids'][ka] = np.append(metadata['well_segment_ids'][ka], N)
                for kb in ['pressure', 'flow_rate']:
                    data['wells'][ka][kb][N] = segment['data'][ka][kb]

            # Add new wells to primary metadata
            if new_wells:
                M = len(new_wells)
                metadata['well_names'] = np.append(metadata['well_names'], new_wells)
                for kb in ['latitude', 'longitude', 'depth', 'easting', 'northing']:
                    tmp = np.empty(M)
                    for ii, kc in enumerate(new_wells):
                        tmp[ii] = data['wells'][kc]['metadata'][kb]
                    metadata[kb] = np.append(metadata[kb], tmp)

                for kb in ['api', 'utm_zone']:
                    tmp = np.empty(M, dtype=str)
                    for ii, kc in enumerate(new_wells):
                        tmp[ii] = data['wells'][kc]['metadata'][kb]
                    metadata[kb] = np.append(metadata[kb], tmp)

        # Update the databases and reload
        self.add_segment_post(data, metadata)
        self.load_data()

    @block_thread
    def add_segment_post(self, data, metadata):
        del self.well_dataset

        # Child database
        root = os.path.abspath(self.database_path)
        fname = os.path.join(root, f'{self.active_source}.hdf5')
        with hdf5_wrapper.hdf5_wrapper(fname, mode='w') as tmp:
            for k, v in data.items():
                tmp[k] = v

        # Parent metadata
        fname = os.path.join(root, 'well_dataset.hdf5')
        with hdf5_wrapper.hdf5_wrapper(fname, mode='a') as tmp:
            tmp[self.active_source]['metadata'] = metadata

    def autopick_external_wells(self, grid, wells):
        if (self.active_source not in self.well_dataset.keys()):
            return

        # grid.process_inputs()
        ca = grid.style_record['Lat Lon']['corner_a']
        cb = grid.style_record['Lat Lon']['corner_b']

        target_metadata = self.well_dataset[self.active_source]['metadata']
        self.logger.info('Adding wells within grid...')
        for ii, well_name in enumerate(target_metadata['well_names']):
            lat = target_metadata['latitude'][ii]
            lon = target_metadata['longitude'][ii]
            if ((lat >= ca[1]) & (lat <= cb[1]) & (lon >= ca[0]) & (lon <= cb[0])):
                self.logger.info(f'  {well_name}')
                if well_name not in wells.children:
                    wells.add_child(well_name)
                new_well = wells.children[well_name]
                new_well.short_name = well_name
                new_well.x = target_metadata['easting'][ii]
                new_well.y = target_metadata['northing'][ii]
                new_well.z = target_metadata['depth'][ii]
                new_well.data_source = self.active_source

        self.update_well_data(grid, wells)

    def get_segment_indices(self, grid):
        segment_indices = []
        segment_start = []
        metadata = self.well_dataset[self.active_source]['metadata']
        ta = metadata['segment_start_time']
        tb = metadata['segment_end_time']

        t_buff = self.grid_buffer_time * 60 * 60 * 24 * 365.25
        self.time_request_start = grid.t_min + grid.t_origin - t_buff
        self.time_request_end = grid.t_max + grid.t_origin + t_buff
        for ii, (tc, td) in enumerate(zip(ta, tb)):
            if ((self.time_request_start < td) & (self.time_request_end > tc)):
                segment_start.append(tc)
                segment_indices.append(str(ii))

        if segment_indices:
            segment_order = np.argsort(segment_start)
            segment_indices = np.array(segment_indices, dtype=str)[segment_order]

        return segment_indices

    def assemble_well_data(self, well_name, segment_indices, grid):
        t = []
        q = []
        metadata = self.well_dataset[self.active_source]['metadata']
        available_ids = list(metadata['well_segment_ids'][well_name])
        ta = self.time_request_start
        tb = self.time_request_end
        segment_epoch = self.well_dataset[self.active_source]['data']['segment_epoch']

        for ii in segment_indices:
            if ii in available_ids:
                w = self.well_dataset[self.active_source]['data']['wells'][well_name]
                well_t = segment_epoch[ii]
                well_q = w['flow_rate'][ii]
                if ((well_t[0] >= ta) & (well_t[-1] <= tb)):
                    t.append(well_t)
                    q.append(well_q)
                else:
                    Ia = np.where(well_t >= ta)[0][0]
                    Ib = np.where(well_t <= tb)[0][-1]
                    t.append(well_t[Ia:Ib])
                    q.append(well_q[Ia:Ib])

        if t:
            t = np.concatenate(t, axis=0)
            q = np.concatenate(q, axis=0)
        else:
            t = np.array([ta, tb])
            q = np.zeros(2)

        return t, q

    @block_thread
    def update_well_data(self, grid, wells):
        if (self.active_source not in self.well_dataset.keys()):
            return

        # Assemble the active well list
        active_wells = []
        for ka, well in wells.children.items():
            if (well.data_source == self.active_source):
                active_wells.append(ka)
        active_wells = sorted(active_wells)

        # Check whether the data request has changed
        dt_a = abs(self.time_request_start - self.last_time_range[0])
        dt_b = abs(self.time_request_end - self.last_time_range[1])
        if ((dt_a < 1e-3) and (dt_b < 1e-3)):
            if active_wells == self.last_well_list:
                return

        # Update the well data
        self.logger.info('Updating well data')
        segment_indices = self.get_segment_indices(grid)
        for ka in active_wells:
            t, q = self.assemble_well_data(ka, segment_indices, grid)
            well = wells.children[ka]
            well.epoch = t
            well.variable_flow_rate = q
            well.init_time = t[0]
            well.flow_rate = q[0]
            well.N = len(t)

        # Record the well list
        self.last_well_list = active_wells
        self.last_time_range = [self.time_request_start, self.time_request_end]

    @block_thread
    def clean_external_wells(self):
        self.logger.info('Removing external well data')
        del self.well_dataset
        dataset_root = os.path.abspath(self.database_path)
        shutil.rmtree(dataset_root)
        self.load_data()

    @block_thread
    def get_plot_location(self, grid):
        x = np.zeros(0)
        y = np.zeros(0)
        z = np.zeros(0)
        if ((self.active_source not in self.well_dataset.keys())):
            return x, y, z

        target_metadata = self.well_dataset[self.active_source]['metadata']
        if ('well_names' in target_metadata.keys()):
            lat = target_metadata['latitude']
            lon = target_metadata['longitude']
            valid_points = np.where((abs(lat) > 0.1) & (abs(lon) > 0.1))[0]
            z = target_metadata['depth'][valid_points] - grid.z_origin
            if (grid.spatial_type == 'UTM'):
                x = target_metadata['easting'][valid_points] - grid.x_origin
                y = target_metadata['northing'][valid_points] - grid.y_origin
            else:
                x = target_metadata['latitude'][valid_points]
                y = target_metadata['longitude'][valid_points]
        return x, y, z

    def get_plot_data(self, projection):
        if self.active_source in self.well_dataset.keys():
            target_metadata = self.well_dataset[self.active_source]['metadata']
            well_names = target_metadata['well_names']
            well_x, well_y, well_z = self.get_plot_location(projection)
            data = {'x': well_x, 'y': well_y, 'z': well_z, 'names': well_names}
            return data

    def well_database_map(self, plot_data):
        well_plot_data = plot_data['Fluid Injection']
        well_database_plot_data = plot_data.get('Well Database')
        grid_plot_data = plot_data['General']

        xr = [grid_plot_data['x'][0] - grid_plot_data['x_origin'], grid_plot_data['x'][-1] - grid_plot_data['x_origin']]
        yr = [grid_plot_data['y'][0] - grid_plot_data['y_origin'], grid_plot_data['y'][-1] - grid_plot_data['y_origin']]
        box = [[xr[0], xr[1], xr[1], xr[0], xr[0]], [yr[0], yr[0], yr[1], yr[1], yr[0]]]

        layers = {}
        if 'x' in well_database_plot_data:
            layers['database_wells'] = {
                'x': well_database_plot_data['x'],
                'y': well_database_plot_data['y'],
                'z': well_database_plot_data['z'],
                't': {
                    'Well': well_database_plot_data['names']
                },
                'type': 'scatter'
            }

        layers['active_wells'] = {
            'x': well_plot_data['x'],
            'y': well_plot_data['y'],
            'z': well_plot_data['z'],
            't': {
                'Well': well_plot_data['names']
            },
            'type': 'scatter'
        }

        layers['box'] = {'x': np.array(box[0]), 'y': np.array(box[1]), 'type': 'line'}

        axes = {
            'x': 'X (m)',
            'y': 'Y (m)',
            'z': 'Z (m)',
        }
        return layers, axes

    def generate_plots(self, **kwargs):
        """
        Generates diagnostic plots for the seismic catalog,
        fluid injection, and forecasts

        """
        # Collect data
        self.logger.debug('Rendering well database plot')
        grid = kwargs.get('grid')
        wells = kwargs.get('wells')

        # Select boundaries
        well_x, well_y, well_z = self.get_plot_location(grid)
        active_x, active_y, active_z = wells.get_plot_location(grid)
        box = [[grid.x_min, grid.x_max, grid.x_max, grid.x_min, grid.x_min],
               [grid.y_min, grid.y_min, grid.y_max, grid.y_max, grid.y_min]]

        # Location plot
        ax = self.figures['spatial_well_database']['handle'].axes[0]
        ax.cla()
        ax.plot(well_x, well_y, label=self.active_source, **gui_colors.alt_well_style)
        ax.plot(active_x, active_y, label='Active Wells', **gui_colors.well_style)
        ax.plot(box[0], box[1], label='Grid boundary', **gui_colors.alt_line_style)
        ax.set_title('Well Locations')
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
        # ax.set_aspect('equal')
        ax.legend(loc=1)
