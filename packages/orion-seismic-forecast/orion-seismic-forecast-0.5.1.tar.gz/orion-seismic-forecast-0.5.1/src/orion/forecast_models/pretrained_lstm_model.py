# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
pretrained_lstm_model.py
---------------------------
"""

from orion import optional_packages
from orion.forecast_models import forecast_model_base
from orion.utilities import hdf5_wrapper
import numpy as np


class PretrainedMachineLearningModel(forecast_model_base.ForecastModel):
    """
    Pretrained Machine Learning forecast model

    Attributes:
        active (bool): Flag to indicate whether the model is active
        forecast_time (ndarray): Time values for forecast calculation
        trained_model_snapshot (str): File name of the saved model (.hdf5)
        trained_model_scaling (str): File name containing model scaling (.hdf5)
        inputs (list): List of input parameters
        outputs (list): List of output parameters
        network (Tensorflow.Model): ML network instance
        scaling (dict): Dict of mean, std for each input/output parameter
    """

    def set_class_options(self, **kwargs):
        """
        Pretrained ML forecasting model initalization
        """
        # Call the parent's initialization
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.active = False
        self.long_name = 'Pretrained LSTM'
        self.short_name = 'ML'
        self.trained_model_snapshot = 'model.hdf5'
        self.trained_model_scaling = 'scaling.hdf5'
        self.inputs = ['test_a', 'test_b']
        self.outputs = ['test_c']

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        super().set_data(**kwargs)
        self.network = None
        self.scaling = {}

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        super().set_gui_options(**kwargs)

        # Configure the gui elements
        self.gui_elements['trained_model_snapshot'] = {
            'element_type': 'entry',
            'label': 'Model Snapshot',
            'position': [3, 0]
        }
        self.gui_elements['trained_model_scaling'] = {
            'element_type': 'entry',
            'label': 'Model Scaling',
            'position': [4, 0]
        }

    def load_model(self):
        """
        Load the machine learning model in a tensorflow-hdf5 format

        """
        from tensorflow import keras
        self.network = keras.models.load_model(self.trained_model_snapshot)
        self.scaling = hdf5_wrapper.hdf5_wrapper(self.trained_model_scaling)

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        # TODO: figure out a standard input/output format
        if 'tensorflow' not in optional_packages:
            self.logger.warning(
                'The optional tensorflow package was not found... skipping pretrained ML forecast model')
            return

        self.load_model()
        model_inputs = {'test_a': np.zeros(10), 'test_b': np.zeros(10)}

        # Scale inputs
        scaled_inputs = [((model_inputs[k] - self.scaling[k]['mean']) / (self.scaling[k]['std'])) for k in self.inputs]
        scaled_inputs = np.moveaxis(np.array(scaled_inputs), 0, -1)

        # Run the model
        scaled_outputs = self.network.predict(scaled_inputs)

        # Scale the outputs
        outputs = {k: np.squeeze(scaled_outputs[:, ii]) for k, ii in zip(self.outputs, range(0, len(self.outputs)))}
        for k in self.outputs:
            outputs[k] = (outputs[k] * self.scaling[k]['std']) + self.scaling[k]['mean']

        # Set the output forecast
        self.logger.debug('    (setting forecast to random array)')
        N = grid.shape
        self.temporal_forecast = np.cumsum(np.random.randint(0, 5, N[3]))
        self.spatial_forecast = np.random.randn(*N)

        return self.temporal_forecast, self.spatial_forecast
