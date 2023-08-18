# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
pretrained_ml_model.py
-----------------------
"""

import numpy as np
from orion.pressure_models import pressure_model_base
from scipy.interpolate import RegularGridInterpolator
import os
import tempfile
import zipfile


class PretrainedMLModel(pressure_model_base.PressureModelBase):
    """
    Pressure model based off of a pre-trained ML network

    Attributes:
        model_path (str): Path to the model file (hdf5)
        input_type (str): Input style string (default = 'K')
        permeability_scale_a (float): Permeability scale factor a
        permeability_scale_b (float): Permeability scale factor b
        injection_scale_a (float): Injection scale factor a
        injection_scale_b (float): Injection scale factor b
        pressure_scale_a (float): Pressure scale factor a
        pressure_scale_b (float): Pressure scale factor c
        p_interp (scipy.interpolate.RegularGridInterpolator): Pressure interpolator
    """

    def set_class_options(self, **kwargs):
        """
        Initialization function

        """
        # Model configuration
        self.short_name = 'PretrainedMLModel'

        # Model snapshot
        self.model_path = ''

        # Model input size / type
        self.available_input_types = ['K', 'K, Qmask']
        self.input_type = self.available_input_types[0]

        # Scale values
        self.permeability_scale_a = 0.0
        self.permeability_scale_b = 0.0
        self.injection_scale_a = 0.0
        self.injection_scale_b = 0.0
        self.pressure_scale_a = 0.0
        self.pressure_scale_b = 0.0

        # Timing values
        self.t_start = 0.0
        self.t_end = 1.0
        self.Nt = 10

        # Note: supress tensorflow warning messages
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        # Interpolator
        self.p_interp = None
        self.dpdt_interp = None

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Gui elements
        self.gui_elements['model_path'] = {
            'element_type': 'entry',
            'command': 'file',
            'label': 'Model path',
            'position': [0, 0],
            'filetypes': [('tensorflow', '*.tf'), ('hdf5', '*.hdf5'), ('all', '*')]
        }

        self.gui_elements['input_type'] = {
            'element_type': 'dropdown',
            'label': 'Inputs',
            'position': [1, 0],
            'values': self.available_input_types
        }

        self.gui_elements['permeability_scale_a'] = {'element_type': 'entry', 'label': 'K scale', 'position': [2, 0]}
        self.gui_elements['permeability_scale_b'] = {
            'element_type': 'entry',
            'units': '(mean, std)',
            'position': [2, 1]
        }
        self.gui_elements['injection_scale_a'] = {'element_type': 'entry', 'label': 'Q scale', 'position': [3, 0]}
        self.gui_elements['injection_scale_b'] = {'element_type': 'entry', 'units': '(mean, std)', 'position': [3, 1]}
        self.gui_elements['pressure_scale_a'] = {'element_type': 'entry', 'label': 'P scale', 'position': [4, 0]}
        self.gui_elements['pressure_scale_b'] = {'element_type': 'entry', 'units': '(mean, std)', 'position': [4, 1]}

        self.gui_elements['t_start'] = {'element_type': 'entry', 'label': 'T range', 'position': [5, 0]}
        self.gui_elements['t_end'] = {'element_type': 'entry', 'units': '(days)', 'position': [5, 1]}

    def __call__(self, x, y, z, t):
        p = 0.0
        if isinstance(x, float):
            # Serial evaluation
            p = self.p_interp([x, y, t])
        else:
            N = np.shape(x)
            points = np.concatenate([
                np.reshape(np.squeeze(x), (-1, 1)),
                np.reshape(np.squeeze(y), (-1, 1)),
                np.reshape(np.squeeze(t), (-1, 1))
            ],
                                    axis=1)
            p = np.reshape(self.p_interp(points), N)
        return p

    def dpdt(self, x, y, z, t):
        dp = 0.0
        if isinstance(x, float):
            # Serial evaluation
            dp = self.dpdt_interp([x, y, t])
        else:
            points = np.concatenate([np.reshape(x, (1, -1)), np.reshape(y, (1, -1)), np.reshape(t, (1, -1))], axis=0)
            dp = self.dpdt_interp(points)
        return dp

    def run(self, grid, well_manager, geologic_model):
        self.logger.debug('Loading tensorflow/keras')
        from tensorflow import keras

        if self.model_path:
            # Check to see if the model needs to be unzipped
            tmp_path = self.model_path
            if ('zip' in self.model_path):
                tmp_dir = tempfile.TemporaryDirectory()
                tmp_path = tmp_dir.name
                self.logger.debug(f'Unzipping the ML model to the following location: {tmp_path}')
                with zipfile.ZipFile(self.model_path, 'r') as zip_ref:
                    zip_ref.extractall(tmp_path)

            # Load the model
            model = keras.models.load_model(tmp_path, compile=False)

            # For now, the model must be consitent with the
            # orion spatial grid dimensions
            Nx = len(grid.x)
            Ny = len(grid.y)

            # The time axis is set via the output shape
            input_shape = model.layers[0].input_shape[0][1:]
            output_shape = model.layers[-1].output_shape[1:]
            Nt = output_shape[0]

            if ((Nx != input_shape[0]) | (Ny != input_shape[1])):
                self.logger.error('There is a mismatch between the orion grid and the ML model inputs:')
                self.logger.error('input_shape = ', input_shape)
                self.logger.error(f'orion spatial grid lengths = ({Nx}, {Ny})')

            # if (Nt != output_shape[0]):
            #   self.logger.error('There is a mismatch between the orion grid and the ML model outputs:')
            #   self.logger.error('output_shape = ', output_shape)
            #   self.logger.error('orion time grid length = %i' % (Nt))

            # Build the inputs
            k = np.zeros((1, Nx, Ny, 1))
            k_interp = geologic_model.permeability
            for ii in range(Nx):
                for jj in range(Ny):
                    k[0, ii, jj, 0] = k_interp(grid.x[ii], grid.y[jj])

            # The inputs are scaled by the min/max values of log(k)
            inputs_scaled = (np.log(k) - self.permeability_scale_a) / (self.permeability_scale_b -
                                                                       self.permeability_scale_a)

            # Run the model
            outputs_scaled = np.squeeze(model.predict(inputs_scaled))

            # The outputs are scaled by the min/max values of pressure
            p = (outputs_scaled * (self.pressure_scale_b - self.pressure_scale_a)) + self.pressure_scale_a

            # The edges of the model seem suspect, so copy the next column in
            self.logger.debug('Modifying edge values for ml-based pressure model')
            p[:, 0, :] = p[:, 1, :]
            p[:, -1, :] = p[:, -2, :]
            p[:, :, 0] = p[:, :, 1]
            p[:, :, -1] = p[:, :, -2]

            # Build the time vector
            t = np.linspace(self.t_start, self.t_end, Nt) * 60 * 60 * 24

            # Calculate the time derivative
            dt = t[1] - t[0]
            tb = t[:-1] + 0.5 * dt
            dpdt = np.diff(p, axis=0) / dt

            # Save the gridded values
            self.p_grid = np.ascontiguousarray(np.expand_dims(np.moveaxis(p, 0, -1), 2))
            self.dpdt_grid = np.ascontiguousarray(np.expand_dims(np.moveaxis(dpdt, 0, -1), 2))
            self.x_grid = grid.x
            self.y_grid = grid.y
            self.z_grid = [0.0]
            self.t_grid = t

            # Convert the points into an interpolator
            self.p_interp = RegularGridInterpolator((self.x_grid, self.y_grid, self.t_grid),
                                                    np.ascontiguousarray(np.squeeze(self.p_grid)),
                                                    bounds_error=False,
                                                    fill_value=None)

            self.dpdt_interp = RegularGridInterpolator((self.x_grid, self.y_grid, tb),
                                                       np.ascontiguousarray(np.squeeze(self.dpdt_grid)),
                                                       bounds_error=False,
                                                       fill_value=None)
