# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
quickstart_wizard.py
--------------------------------------
"""

from orion.gui.wizard_base import OrionWizardStepBase, WizardBase
from orion.gui.custom_widgets import open_link_factory
from orion.utilities import other, timestamp_conversion, unit_conversion
import numpy as np
import utm
import os

units = unit_conversion.UnitManager()


class QuickstartWizard(WizardBase):
    """
    Wizard base class
    """

    def __init__(self, *xargs, **kwargs):
        """
        Orion information gui initialization
        """
        # Call the parent's initialization
        super().__init__(*xargs, **kwargs)
        self.wizard_first_step_class = UserIdentificationStep

        # Key information to collect
        self.user = ''
        self.distance_units = 'km'
        self.time_units = 'days'
        self.wells_to_add = 0
        self.well_index = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.address = ''
        self.well_region = ''
        self.download_well_data = 'No'
        self.radius = 100.0
        self.ref_time = 0.0
        self.time_past = 100.0
        self.time_future = 100.0
        self.ask_flow_rate = False
        self.dimension_option = '3D'

        self.utm_zone = ''
        self.origin = np.zeros(3)

        # Unit information
        self.unit_scale = {}

        # Reset data in orion
        self.parent.orion_manager.clear_data_recursive()

        # Start the wizard
        self.parent.pre_load_update()
        self.create_main()
        self.lift()

        # Set the status
        self.status.set('')
        self.updater()

    def quit(self):
        # Load new data and update the screen
        orion_manager = self.parent.orion_manager
        grid_manager = orion_manager.children["GridManager"]
        orion_manager.load_data(grid_manager)
        self.parent.post_load_update()
        super().quit()

    def wizard_finalize(self):
        # Update values in Orion
        orion_manager = self.parent.orion_manager
        orion_manager.snapshot_time = 0.0
        orion_manager.user_type = self.user
        orion_manager.set_plot_visibility()

        # Skip this step for operators and super users
        if self.user in ['Operator', 'Super User']:
            self.parent.post_load_update()
            return

        # Parse time values
        ts = ''
        if self.ref_time > 0.0:
            ts = timestamp_conversion.get_time_string(self.ref_time)
        else:
            ts = timestamp_conversion.get_current_time_string()
        dt = (self.time_future + self.time_past) / 100.0

        # Parse spatial values
        r = self.radius
        value_scale = {'m': 1.0, 'km': 1e3, 'miles': 1609.34, 'ft': 0.3048, 'degrees (lat/lon)': 1.0}
        r *= value_scale[self.distance_units]
        dr = r / 10.0
        x = self.latitude
        y = self.longitude
        spatial_type = 'Lat Lon'
        self.utm_zone = '16S'
        if 'degrees' not in self.distance_units:
            spatial_type = 'UTM'
            tmp = list(utm.from_latlon(self.latitude, self.longitude))
            x = tmp[0]
            y = tmp[1]
            self.utm_zone = str(tmp[2]) + tmp[3]

        # Set grid values
        grid_manager = orion_manager.children["GridManager"]
        grid_manager.ref_time_str = ts
        grid_manager.t_min_input = -self.time_past
        grid_manager.t_max_input = self.time_future
        grid_manager.plot_time_min = -self.time_past
        grid_manager.plot_time_max = self.time_future
        grid_manager.dt_input = dt
        grid_manager.spatial_type = spatial_type
        grid_manager.utm_zone = self.utm_zone
        grid_manager.x_origin = x
        grid_manager.y_origin = y
        grid_manager.z_origin = 0.0
        grid_manager.x_min = -r
        grid_manager.x_max = r
        grid_manager.dx = dr
        grid_manager.y_min = -r
        grid_manager.y_max = r
        grid_manager.dy = dr
        grid_manager.z_min = 0.0
        grid_manager.z_max = 1.0
        grid_manager.dz = 1.0

        catalog = orion_manager.children["SeismicCatalog"]
        catalog.use_comcat = 1
        catalog.catalog_source = ""

        pressure_manager = orion_manager.children["PressureManager"]
        pressure_manager.active_model_name = 'RadialFlowModel'

        well_manager = orion_manager.children["WellManager"]
        well_manager.clear_wells()
        well_manager.add_child('Well_01')
        w = well_manager.children['Well_01']
        w.x = grid_manager.x_origin + grid_manager.x_min - 1e4
        w.y = grid_manager.y_origin + grid_manager.y_min - 1e4
        w.z = 0.0

        appearance_manager = orion_manager.children["AppearanceManager"]
        appearance_manager.add_map_layer = True
        appearance_manager.allow_self_signed_certs = True

        if self.download_well_data == 'Yes':
            well_database = orion_manager.children["WellDatabase"]
            well_database.active_source = self.well_region

            ra = timestamp_conversion.convert_timestamp(grid_manager.ref_time_str)
            ra -= (self.time_past + 365.25) * 60 * 60 * 24
            rb = timestamp_conversion.get_time_string(ra)
            well_database.external_request_start = rb
            self.status.set('Download')
            well_database.load_data(grid_manager)
            well_database.update_external_data()
            self.status.set('Picking')
            well_database.autopick_external_wells(grid_manager, well_manager)
            self.status.set('')

        # Request data processing
        self.parent.request_all()


class UserIdentificationStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Welcome to the ORION tool!'

        # Setup options
        self.options = {
            'Understand earthquake activity in my community': 'General',
            'Determine whether an event I felt was due to injection': 'Specific Earthquake',
            'Communicate with others about earthquake risk in my community': 'General',
            'Understand how injection influences earthquake activity': 'Operator',
            'Determine the earthquake risks for a current/planned injection': 'Operator',
            'Determine how long an injection will likely cause earthquakes': 'Operator',
            'Evaluate the impact of injection scenarios on seismic activity': 'Operator',
            'See what models are used in ORION and how I can use them': 'Super User',
            'Use this tool for a research project': 'Super User'
        }

        general_steps = [GeneralUserStep, SearchRadiusStep]
        specific_eq_steps = [SpecificEarthquakeStep, SearchRadiusStep]
        operator_steps = [OperatorDataInventory]
        superuser_steps = [SuperUserOptions]

        self.option_map = {
            'General': general_steps,
            'Specific Earthquake': specific_eq_steps,
            'Operator': operator_steps,
            'Super User': superuser_steps
        }
        self.option_names = list(self.options.keys())
        self.current_option = self.option_names[0]
        self.time_unit_options = ['seconds', 'days', 'years']
        self.time_units = self.time_unit_options[1]
        self.spatial_unit_options = ['km', 'm', 'miles', 'ft', 'degrees (lat/lon)']
        self.distance_units = self.spatial_unit_options[0]

        # Add elements
        self.wizard_elements['current_option'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'How would you like to use this tool?',
                'values': self.option_names,
                'position': [1, 0],
                'width': 50
            }
        }
        self.wizard_elements['time_units'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'What time units would you like to use?',
                'values': self.time_unit_options,
                'position': [2, 0],
                'width': 20
            }
        }
        self.wizard_elements['distance_units'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'What distance units would you like to use?',
                'values': self.spatial_unit_options,
                'position': [3, 0],
                'width': 20
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.distance_units = self.distance_units
        self.parent.time_units = self.time_units
        user_type = self.options[self.current_option]
        self.parent.user = user_type

        # Choose next steps
        next_steps = self.option_map[user_type]
        self.parent.queue_steps(next_steps)


class GeneralUserStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What location are you interested in?'

        # Add options
        self.location_str = ''
        self.invalid_str_message = '(enter a valid location)'

        # Add elements
        self.wizard_elements['location_str'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Location:',
                'units': 'Zip Code or GPS Coordinates (latitude, longitude)',
                'position': [1, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        if not self.location_str:
            self.location_str = self.invalid_str_message
            return 'Location string is empty'

        tmp = other.parse_location_str(self.location_str)
        if tmp:
            self.parent.latitude = tmp[0]
            self.parent.longitude = tmp[1]
            self.parent.address = tmp[2]
        else:
            self.location_str = self.invalid_str_message
            return 'Location string is invalid'


class SpecificEarthquakeStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Tell us more when and where you felt the earthquake:'

        # Add options
        self.search_days = 7.0
        self.location_str = ''
        self.or_str = 'or'
        self.usgs_map_url = 'https://earthquake.usgs.gov/earthquakes/map/?extent=9.53736,-146.33789&extent=57.23239,-39.46289&range=week&magnitude=all&baseLayer=street'
        self.usgs_event_page_url = ''
        self.invalid_str_message = '(enter a valid location)'
        self.invalid_id_message = '(earthquake not found)'

        # Add elements
        self.wizard_elements['search_days'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'I felt it within the last',
                'position': [1, 0],
                'units': 'days'
            }
        }
        self.wizard_elements['location_str'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Where did you feel it?',
                'units': 'Zip Code or GPS Coordinates (latitude, longitude)',
                'position': [2, 0]
            }
        }
        self.wizard_elements['or_str'] = {'parent': self, 'config': {'element_type': 'text', 'position': [3, 0]}}
        self.wizard_elements['usgs_event_page_url'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Provide the USGS URL or ID',
                'callback': open_link_factory(self.usgs_map_url),
                'text': 'Open Map',
                'position': [4, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        # Load the target event
        if self.usgs_event_page_url:
            event = other.parse_usgs_event_page(self.search_days, self.usgs_event_page_url)
            if event:
                self.parent.ref_time = event[0]
                self.parent.latitude = event[1]
                self.parent.longitude = event[2]
                tmp = other.parse_location_str(f'{self.parent.latitude}, {self.parent.longitude}')
                if tmp:
                    self.parent.address = tmp[2]
            else:
                self.usgs_event_page_url = self.invalid_id_message
                return "Earthquake not found"
        elif self.location_str:
            tmp = other.parse_location_str(self.location_str)
            if tmp:
                self.parent.latitude = tmp[0]
                self.parent.longitude = tmp[1]
                self.parent.address = tmp[2]
            else:
                self.location_str = self.invalid_str_message
                return 'Location string is invalid'
        else:
            self.logger.error('Either a location or USGS page should be specified')
            return 'ID and location strings are empty'


class SearchRadiusStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'How large of an area and time range are you interested in?'

        # Add options
        self.search_radius = 100.0
        self.time_past = 100.0
        self.time_future = 0.0
        self.well_data_regions = {'Oklahoma': 'OK_Corp_Commission'}

        # Add elements
        self.wizard_elements['search_radius'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Distance to search for events',
                'units': self.parent.distance_units,
                'position': [1, 0]
            }
        }
        self.wizard_elements['time_past'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Time to search for events in the past',
                'units': self.parent.time_units,
                'position': [2, 0]
            }
        }
        self.wizard_elements['time_future'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Time to forecast earthquake activity in the future',
                'units': self.parent.time_units,
                'position': [3, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.time_past = self.time_past
        self.parent.time_future = self.time_future
        self.parent.radius = self.search_radius

        for k, v in self.well_data_regions.items():
            if k in self.parent.address:
                self.parent.well_region = v
                self.parent.queue_steps([GeneralWellDatabase])


class GeneralWellDatabase(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Do you want to download well information for the target area?'

        # Add options
        self.download_options = ['Yes', 'No']
        self.download_well_data = self.download_options[0]

        # Add elements
        self.wizard_elements['download_well_data'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'values': self.download_options,
                'units': '(Note: this may take a few minutes)',
                'position': [2, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.download_well_data = self.download_well_data


class OperatorDataInventory(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What data do you have access to?'

        self.operator_data = {
            'Well Locations': False,
            'Injection / Extraction Well Flow Rates': False,
            'Pre-existing Pressure Model': False,
            'Earthquake Catalog': False
        }

        # Add elements
        self.wizard_elements['operator_data'] = {
            'parent': self,
            'config': {
                'element_type': 'checkbox',
                'header': 'Select all that apply:',
                'ncol': 1,
                'position': [1, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.queue_steps([ReferenceTimeStep, OperatorLocationStep, OperatorGridStep])

        if self.operator_data['Earthquake Catalog']:
            self.parent.queue_steps(CatalogStep)

        if self.operator_data['Well Flow Rates']:
            self.parent.queue_steps(RadialFlowStep)
            self.parent.ask_flow_rate = True

        if self.operator_data['Pre-existing Pressure Model']:
            self.parent.queue_steps(PressureModelStep)

        if self.operator_data['Well Locations']:
            self.parent.queue_steps(WellNumberStep)


class SuperUserOptions(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Select key ORION options:'

        # Add elements
        available_time_options = ['Current Time', 'Epoch', 'Time String']
        available_catalog_options = ['Local File', 'ComCat']
        available_dimension_options = ['2D (xy)', '3D']
        self.time_option = available_time_options[0]
        self.catalog_option = available_catalog_options[0]
        self.dimension_option = available_dimension_options[0]

        self.wizard_elements['time_option'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'Reference time',
                'position': [1, 0],
                'values': available_time_options
            }
        }
        self.wizard_elements['spatial_type'] = {
            'parent': self.parent.parent.orion_manager.children['GridManager'],
            'config': {
                'position': [2, 0]
            }
        }
        self.wizard_elements['dimension_option'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'Problem type',
                'position': [3, 0],
                'values': available_dimension_options
            }
        }
        self.wizard_elements['catalog_option'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'Seismic catalog type',
                'position': [4, 0],
                'values': available_catalog_options
            }
        }
        self.wizard_elements['active_model_name'] = {
            'parent': self.parent.parent.orion_manager.children['PressureManager'],
            'config': {
                'position': [5, 0]
            }
        }

    def finalize_step(self):
        """
        Check step values
        """
        self.parent.dimension_option = self.dimension_option
        self.parent.queue_steps([ReferenceTimeStep, SuperUserGridStep])

        if self.catalog_option == 'Local File':
            self.parent.queue_steps(CatalogStep)

        p = self.parent.parent.orion_manager.children['PressureManager']
        if p.active_model_name == 'RadialFlowModel':
            self.parent.queue_steps([RadialFlowStep, WellNumberStep])
        else:
            self.parent.queue_steps([PressureModelStep, WellNumberStep])


class CatalogStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What is the path of the seismic catalog on the local machine?'

        self.wizard_elements['catalog_source'] = {
            'parent': self.parent.parent.orion_manager.children['SeismicCatalog'],
            'config': {
                'label': 'Catalog',
                'width': 30,
                'position': [1, 0]
            }
        }

    def finalize_step(self):
        """
        Check step values
        """
        f = self.parent.parent.orion_manager.children['SeismicCatalog'].catalog_source
        if not os.path.isfile(f):
            err = f"Specified catalog file was not found: {f}"
            return err


class PressureModelStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What is the path of the pressure model on the local device?'
        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        pressure_manager.active_model_name = 'PressureTableModel'

        self.wizard_elements['file_name'] = {
            'parent': pressure_manager.children['PressureTableModel'],
            'config': {
                'position': [1, 0],
                'label': 'Pressure table file:'
            }
        }

    def finalize_step(self):
        """
        Check step values
        """
        # Check the pressure model file
        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        f = pressure_manager.children['PressureTableModel'].file_name
        if not (os.path.isfile(f) or os.path.isdir(f)):
            err = f"Specified pressure model was not found: {f}"
            return err


class RadialFlowStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What are the average hydraulic properties of the reservoir?'

        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        rfm = pressure_manager.children['RadialFlowModel']
        pressure_manager.active_model_name = 'RadialFlowModel'

        self.wizard_elements['viscosity'] = {'parent': rfm, 'config': {'position': [1, 0]}}
        self.wizard_elements['permeability'] = {'parent': rfm, 'config': {'position': [2, 0]}}
        self.wizard_elements['storativity'] = {'parent': rfm, 'config': {'position': [3, 0]}}
        self.wizard_elements['payzone_thickness'] = {'parent': rfm, 'config': {'position': [4, 0]}}


class ReferenceTimeStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Time Options'

        self.wizard_elements['ref_time_str'] = {
            'parent': self.parent.parent.orion_manager.children['GridManager'],
            'config': {
                'position': [1, 0]
            }
        }


class OperatorLocationStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Where would you like to place the center of the grid?'
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        xy_units = self.parent.distance_units
        z_units = xy_units.copy()
        if 'degrees' in xy_units:
            z_units = 'm'

        # Add elements
        self.wizard_elements['x'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'position': [1, 0],
                'label': 'Origin'
            }
        }
        self.wizard_elements['y'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'position': [1, 1],
                'units': f'({xy_units})'
            }
        }
        self.wizard_elements['z'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'position': [2, 0],
                'label': 'Depth',
                'units': f'({z_units})'
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.origin = np.array([self.x, self.y, self.z])


class OperatorGridStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'How large of a grid would you like to use?'
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
        xy_units = self.parent.distance_units
        z_units = xy_units.copy()
        if 'degrees' in xy_units:
            z_units = 'm'

        # Add elements
        self.wizard_elements['dx'] = {'parent': self, 'config': {'position': [1, 0], 'label': 'Extents'}}
        self.wizard_elements['dy'] = {'parent': self, 'config': {'position': [1, 1], 'units': f'({xy_units})'}}
        self.wizard_elements['dz'] = {
            'parent': self,
            'config': {
                'position': [1, 2],
                'label': 'Depth',
                'units': f'({z_units})'
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        grid_manager = self.parent.parent.orion_manager.children['GridManager']
        grid_manager.x_origin = self.parent.origin[0]
        grid_manager.y_origin = self.parent.origin[1]
        grid_manager.z_origin = self.parent.origin[2]
        grid_manager.utm_zone = self.parent.utm_zone
        grid_manager.x_min = self.parent.origin[0]
        grid_manager.y_min = self.parent.origin[1]
        grid_manager.z_min = self.parent.origin[2]

        # [self.x_origin, self.y_origin]
        # [self.x_min + self.x_origin, self.y_min + self.y_origin]
        # [self.x_max + self.x_origin, self.y_max + self.y_origin]
        # [self.dx, self.dy]

        # if 'degrees' in self.parent.distance_units:
        #     self.spatial_type
        #     tmp = list(utm.from_latlon(self.x, self.y))
        #     self.parent.origin = np.array([tmp[0], tmp[1], self.z])
        #     self.parent.utm_zone = str(tmp[2]) + tmp[3]
        # else:
        #     self.parent.origin = np.array([self.x, self.y, self.z])
        #     self.parent.origin *= units[self.distance_units]


class SuperUserGridStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Spatial Grid'

        # Simplify the grid boundaries
        grid_manager = self.parent.parent.orion_manager.children['GridManager']
        grid_manager.x_min = 0.0
        grid_manager.y_min = 0.0
        grid_manager.z_min = 0.0

        # Setup simple labels
        self.dimension = self.parent.dimension_option
        spatial_labels = {'UTM': ['East (m)', 'North (m)'], 'Lat Lon': ['Longitude (o)', 'Latitude (o)']}
        xy_labels = spatial_labels[grid_manager.spatial_type]
        z_labels = 'Depth (m)'

        # Add elements
        self.wizard_elements['x_origin'] = {
            'parent': grid_manager,
            'config': {
                'position': [1, 0],
                'units': xy_labels[0],
                'label': 'Origin'
            }
        }
        self.wizard_elements['y_origin'] = {
            'parent': grid_manager,
            'config': {
                'position': [1, 1],
                'units': xy_labels[1],
                'label': ''
            }
        }
        self.wizard_elements['x_max'] = {
            'parent': grid_manager,
            'config': {
                'position': [2, 0],
                'units': xy_labels[0],
                'label': 'Grid size'
            }
        }
        self.wizard_elements['y_max'] = {
            'parent': grid_manager,
            'config': {
                'position': [2, 1],
                'units': xy_labels[1],
                'label': ''
            }
        }
        self.wizard_elements['dx'] = {
            'parent': grid_manager,
            'config': {
                'position': [3, 0],
                'units': xy_labels[0].split()[1],
                'label': 'Grid resolution:'
            }
        }
        self.wizard_elements['dy'] = {
            'parent': grid_manager,
            'config': {
                'position': [3, 1],
                'units': xy_labels[1].split()[1],
                'label': ''
            }
        }

        if self.dimension == '3D':
            self.wizard_elements['z_origin'] = {
                'parent': grid_manager,
                'config': {
                    'position': [1, 2],
                    'units': z_labels,
                    'label': ''
                }
            }
            self.wizard_elements['z_max'] = {
                'parent': grid_manager,
                'config': {
                    'position': [2, 2],
                    'units': z_labels,
                    'label': ''
                }
            }
            self.wizard_elements['dz'] = {
                'parent': grid_manager,
                'config': {
                    'position': [3, 2],
                    'units': z_labels.split()[1],
                    'label': ''
                }
            }

        else:
            self.wizard_elements['z_max'] = {
                'parent': grid_manager,
                'config': {
                    'position': [4, 0],
                    'label': 'Reservoir thickness',
                    'units': z_labels.split()[1]
                }
            }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        grid_manager = self.parent.parent.orion_manager.children['GridManager']
        if self.dimension == '2D (xy)':
            grid_manager.dz = grid_manager.z_max


class WellNumberStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'How many wells would you like to add?'
        self.wells_to_add = 0
        self.wizard_elements['wells_to_add'] = {
            'parent': self,
            'config': {
                'position': [5, 0],
                'element_type': 'entry',
                'label': 'Number of wells'
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        if self.wells_to_add > 0:
            for ii in range(self.wells_to_add):
                self.parent.queue_steps(WellInformationStep)


class WellInformationStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = f'Please enter the information about well {self.parent.well_index + 1}'
        self.well_name = ''
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.flow_rate = 0.0
        self.init_time = '0'
        self.or_label = 'or'
        self.flow_file = ''

        self.wizard_elements['well_name'] = {
            'parent': self,
            'config': {
                'position': [1, 0],
                'element_type': 'entry',
                'label': 'Name'
            }
        }
        self.wizard_elements['x'] = {
            'parent': self,
            'config': {
                'position': [2, 0],
                'element_type': 'entry',
                'label': 'Wellhead location'
            }
        }
        self.wizard_elements['y'] = {
            'parent': self,
            'config': {
                'position': [2, 0],
                'element_type': 'entry',
                'units': '(latitude, longitude) or (eastings, northings)'
            }
        }
        self.wizard_elements['z'] = {
            'parent': self,
            'config': {
                'position': [3, 0],
                'element_type': 'entry',
                'label': 'Depth'
            }
        }

        if self.parent.ask_flow_rate:
            self.wizard_elements['flow_rate'] = {
                'parent': self,
                'config': {
                    'position': [4, 0],
                    'element_type': 'entry',
                    'label': 'Average flow rate',
                    'units': '(m3/s)'
                }
            }
            self.wizard_elements['init_time'] = {
                'parent': self,
                'config': {
                    'position': [5, 0],
                    'element_type': 'entry',
                    'label': 'Pump start time',
                    'units': self.parent.time_units
                }
            }
            self.wizard_elements['or_label'] = {'parent': self, 'config': {'position': [6, 0], 'element_type': 'text'}}
            self.wizard_elements['flow_file'] = {
                'parent': self,
                'config': {
                    'position': [7, 0],
                    'element_type': 'entry',
                    'label': 'Flow file',
                    'filetypes': [('csv', '*.csv'), ('all', '*')]
                }
            }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.well_index += 1

        well_manager = self.parent.parent.orion_manager.children['WellManager']
        well_manager.add_child(self.well_name)
        well = well_manager.children[self.well_name]
        well.short_name = self.well_name
        well.x = self.x
        well.y = self.y
        well.z = self.z
        well.flow_rate = self.flow_rate
        well.init_time_input = self.init_time
        well.fname = self.flow_file
