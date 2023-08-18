# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import pytest
import numpy as np
import os
import tempfile
from scipy.stats import pareto
import sys
from pathlib import Path

package_path = os.path.abspath(Path(__file__).resolve().parents[1])
mod_path = os.path.abspath(os.path.join(package_path, 'src'))
sys.path.append(mod_path)
strive_path = os.path.abspath(os.path.join(package_path, '..', 'strive', 'src'))
sys.path.append(strive_path)


class TestSeismicCatalog():

    @pytest.fixture(scope='class')
    def grid(self):
        from orion.managers import grid_manager
        grid_manager = grid_manager.GridManager()
        grid_manager.process_inputs()
        return grid_manager

    @pytest.fixture(scope='class')
    def paths(self):
        temp_dir = tempfile.TemporaryDirectory()
        fname = os.path.join(temp_dir.name, 'catalog.csv')
        return temp_dir, fname

    @pytest.fixture(scope='class')
    def catalog(self, grid, paths):
        from orion.managers import seismic_catalog
        catalog = seismic_catalog.SeismicCatalog()
        catalog.catalog_source = paths[1]
        catalog.test_metadata = self.write_example_catalog(paths[1])
        return catalog

    def write_example_catalog(self, fname, utm_zone='10S', b=0.9, N=5000):
        # Write the catalog
        np.random.seed(12345)
        header = f'utm_zone, {utm_zone}\nmagnitude, easting, northing, depth, epoch'
        m = np.log10(pareto.rvs(b, size=N))
        x = 5e5 + (np.random.random(N) * 1000.0)
        y = 6e5 + (np.random.random(N) * 1000.0)
        z = np.random.random(N) * 1000.0
        t = np.cumsum(abs(np.random.randn(N))) * 100
        data = np.transpose(np.array([m, x, y, z, t]))
        np.savetxt(fname, data, header=header, delimiter=',', comments='')

        # Record some catalog characteristics for testing
        dt = np.diff(t)
        m = {
            't_min': t[0],
            't_max': t[-1],
            'm_min': np.amin(m),
            'm_max': np.amax(m),
            'target_dt': 0.5 * (np.amin(dt) + np.amax(dt))
        }
        return m

    def get_catalog_params(self, c):
        t = c.relative_time
        magnitude = c.magnitude_slice
        return np.amin(t), np.amax(t), np.amin(magnitude), np.amax(magnitude), np.amin(np.diff(t))

    def check_value_with_tolerance(self, value, expected, atol=1e-6):
        assert value == pytest.approx(expected, abs=atol)

    def test_a_load_catalog(self, catalog, grid):
        catalog.load_data(grid)
        assert len(catalog) == 5000

    def test_b_check_reset_slice(self, catalog):
        catalog.reset_slice()
        r = self.get_catalog_params(catalog)
        self.check_value_with_tolerance(r[0], catalog.test_metadata['t_min'])
        self.check_value_with_tolerance(r[1], catalog.test_metadata['t_max'])
        self.check_value_with_tolerance(r[2], catalog.test_metadata['m_min'])
        self.check_value_with_tolerance(r[3], catalog.test_metadata['m_max'])

    def test_c_check_time_slice(self, catalog):
        t_mid = 0.5 * (catalog.test_metadata['t_min'] + catalog.test_metadata['t_max'])
        catalog.set_slice(time_range=[-1e9, t_mid])
        r = self.get_catalog_params(catalog)
        self.check_value_with_tolerance(r[0], catalog.test_metadata['t_min'])
        assert r[1] <= t_mid

    def test_d_check_magnitude_slice(self, catalog):
        m_mid = 0.5 * (catalog.test_metadata['m_min'] + catalog.test_metadata['m_max'])
        catalog.set_slice(magnitude_range=[-1e9, m_mid])
        r = self.get_catalog_params(catalog)
        self.check_value_with_tolerance(r[2], catalog.test_metadata['m_min'])
        assert r[3] <= m_mid

    def test_d_check_combined_slice(self, catalog):
        ta = 0.235 * (catalog.test_metadata['t_min'] + catalog.test_metadata['t_max'])
        tb = 0.689 * (catalog.test_metadata['t_min'] + catalog.test_metadata['t_max'])
        ma = 0.12 * (catalog.test_metadata['m_min'] + catalog.test_metadata['m_max'])
        mb = 0.546 * (catalog.test_metadata['m_min'] + catalog.test_metadata['m_max'])
        catalog.set_slice(time_range=[ta, tb], magnitude_range=[ma, mb])
        r = self.get_catalog_params(catalog)
        assert r[0] >= ta
        assert r[1] <= tb
        assert r[2] >= ma
        assert r[3] <= mb

    def test_e_check_minimum_intervenant_time_slice(self, catalog):
        ta = 0.235 * (catalog.test_metadata['t_min'] + catalog.test_metadata['t_max'])
        tb = 0.689 * (catalog.test_metadata['t_min'] + catalog.test_metadata['t_max'])
        ma = 0.12 * (catalog.test_metadata['m_min'] + catalog.test_metadata['m_max'])
        mb = 0.546 * (catalog.test_metadata['m_min'] + catalog.test_metadata['m_max'])
        catalog.set_slice(time_range=[ta, tb],
                          magnitude_range=[ma, mb],
                          minimum_interevent_time=catalog.test_metadata['target_dt'])
        r = self.get_catalog_params(catalog)
        assert r[0] >= ta
        assert r[1] <= tb
        assert r[2] >= ma
        assert r[3] <= mb
        assert r[4] >= catalog.test_metadata['target_dt']

    def test_f_gutenberg_richter_positive(self, catalog):
        from orion.managers import seismic_catalog

        catalog.reset_slice()
        m = catalog.magnitude_slice
        b = seismic_catalog.gutenberg_richter_b_positive(m)
        self.check_value_with_tolerance(b, 1.177220974835335)

    def test_g_mc_bvs(self, catalog):
        from orion.managers import seismic_catalog

        catalog.reset_slice()
        m = catalog.magnitude_slice
        mc = seismic_catalog.mbs(m, mbin=0.1)
        self.check_value_with_tolerance(mc[0], 0.10005175934766876)

    def test_h_gutenberg_richter_mle(self, catalog):
        from orion.managers import seismic_catalog

        catalog.reset_slice()
        m = catalog.magnitude_slice
        b = seismic_catalog.gutenberg_richter_b_mle(m)
        self.check_value_with_tolerance(b, 1.0172016590779172)

    def test_i_gutenberg_richter_a_value(self, catalog):
        # TODO: Add a test for a-value calculations
        self.check_value_with_tolerance(1.0, 1.0)
