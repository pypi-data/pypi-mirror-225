from os import path
import glob
import numpy as np
from zipfile import ZipFile
import tempfile
import numpy as np
from scipy import interpolate    # type: ignore[import]


class OpenIAMParser():

    def __init__(self, fname, **kwargs):
        self.data_dir = fname
        self.t = []
        self.Nt = 0
        self.Ndim = 1
        self.points = []
        self.properties = {}
        self.iterator_keys = []
        self.iterator_step = 0
        self.time_interpolator = None
        self.linear_interpolator = None
        self.nearest_interpolator = None

        self.time_scale = kwargs.get('time_scale', 1.0)
        self.time_offset = kwargs.get('time_offset', 1.0)
        self.spatial_scale = kwargs.get('spatial_scale', 1.0)
        self.spatial_offset = kwargs.get('spatial_offset', np.zeros(3))

        self._load_data()
        self._build_interpolators()

    def _load_data(self):
        # Check if the target exists and if it needs to be unzipped
        if path.isfile(self.data_dir):
            if self.data_dir[-4:] == '.zip':
                zipfile = ZipFile(self.data_dir)
                self.data_dir = tempfile.mkdtemp()
                zipfile.extractall(self.data_dir)
            else:
                raise Exception(f'Unrecognized file extension: {self.data_dir}')
        elif not path.isdir(self.data_dir):
            raise FileNotFoundError(f'File not found: {self.data_dir}')

        # Load time data
        time_file = path.join(self.data_dir, 'time_points.csv')
        if not path.isfile(time_file):
            raise FileNotFoundError('time_points.csv not found in the OpenIAM output')
        self.t = (np.loadtxt(time_file, delimiter=',') + self.time_offset) * self.time_scale

        # Load grid data
        grid_file = ''
        csv_files = [f for f in glob.glob(path.join(self.data_dir, '*.csv')) if 'time_points' not in f]
        N = len(csv_files)
        if (N == 0):
            raise FileNotFoundError('OpenIAM grid file not found in the target directory')
        elif (N == 1):
            grid_file = csv_files[0]
        else:
            raise FileNotFoundError('More than one potential OpenIAM grid file found in the target directory')

        header = open(grid_file, 'r').readline().strip('#').strip().split(',')
        data = {k: x for k, x in zip(header, np.loadtxt(grid_file, delimiter=',', unpack=True, skiprows=1))}

        # Find spatial axes
        for k, offset in zip(['x', 'y', 'z'], self.spatial_offset):
            if k in data.keys():
                self.Ndim += 1
                tmp = (data.pop(k) + offset) * self.spatial_scale
                self.points.append(tmp)
        self.points = np.swapaxes(np.array(self.points), 0, 1)

        # Find property names and build the template interpolators
        self.Nt = len(self.t)
        property_names = np.unique([k[:k.rfind('_')] for k in data.keys()])
        for k in property_names:
            self.properties[k] = [np.ascontiguousarray(data[f'{k}_{ii + 1}']) for ii in range(self.Nt)]

    def _build_interpolators(self):
        time_index = np.linspace(0, self.Nt - 1, self.Nt)
        v = np.zeros(len(self.points))
        self.time_interpolator = interpolate.interp1d(self.t,
                                                      time_index,
                                                      bounds_error=False,
                                                      fill_value=(0, self.Nt - 1))
        self.linear_interpolator = interpolate.LinearNDInterpolator(self.points, v)
        self.nearest_interpolator = interpolate.NearestNDInterpolator(self.points, v)

    def _update_interpolators_snapshot(self, k, time_index):
        self.linear_interpolator.values = np.expand_dims(self.properties[k][time_index], -1)
        self.nearest_interpolator.values = self.properties[k][time_index]

    def _get_time_indeces_weight(self, t):
        x = self.time_interpolator(t)
        Ia = np.floor(x)
        if isinstance(Ia, np.ndarray):
            Ia = Ia.astype(int)
        else:
            Ia = int(Ia)

        Ib = np.minimum(Ia + 1, self.Nt - 1)
        wb = x - Ia
        wa = 1.0 - wb
        return (Ia, Ib), (wa, wb)

    def _interpolate_scalar(self, property_name, spatial_args, t):
        v = 0.0
        for ii, w in zip(*self._get_time_indeces_weight(t)):
            self._update_interpolators_snapshot(property_name, ii)
            x = self.linear_interpolator(spatial_args)
            if np.isnan(x):
                x = self.nearest_interpolator(spatial_args)
            v += w * x
        return v

    def _interpolate_array(self, property_name, spatial_args, t):
        v = np.zeros(np.shape(spatial_args[0]))
        for ii, w in zip(*self._get_time_indeces_weight(t)):
            self._update_interpolators_snapshot(property_name, ii)
            x = self.linear_interpolator(spatial_args)
            Ia = np.isnan(x)
            if np.sum(Ia):
                y = self.nearest_interpolator(spatial_args)
                x[Ia] = y[Ia]
            v += w * x
        return v

    def _interpolate_time(self, property_name, spatial_args, time_args):
        v = np.zeros(len(time_args))
        indices, weights = self._get_time_indeces_weight(time_args)
        for ii, t in enumerate(time_args):
            for jj in [0, 1]:
                self._update_interpolators_snapshot(property_name, indices[jj][ii])
                x = self.linear_interpolator(spatial_args)
                if np.isnan(x):
                    x = self.nearest_interpolator(spatial_args)
                v[ii] += weights[jj][ii] * x
        return v

    def _interpolate_gridded(self, property_name, spatial_args, time_args):
        v = np.zeros(np.shape(spatial_args[0]))

        # Trim the arg list (assume Fortran-style indexing)
        grid_args = tuple([x[..., 0] for x in spatial_args])
        Nt = np.shape(time_args)[-1]
        time_args = np.reshape(time_args, (-1))[:Nt]

        # Interpolate for time slices
        for ii, t in enumerate(time_args):
            v[..., ii] += self._interpolate_array(property_name, grid_args, t)
        return v

    def __call__(self, k, *xargs):
        # Collect the args
        if len(xargs) != self.Ndim:
            raise Exception(f'The interpolator requires arguments equal to the number of dimensions ({self.Ndim})')
        spatial_args = xargs[:self.Ndim - 1]
        time_args = xargs[-1]

        # Check arg dimensions
        arg_dims = np.zeros(len(xargs), dtype=int)
        for ii, x in enumerate(xargs):
            if isinstance(x, np.ndarray):
                arg_dims[ii] = x.ndim

        if arg_dims[-1]:
            if np.any(arg_dims[:-1]):
                return self._interpolate_gridded(k, spatial_args, time_args)
            else:
                return self._interpolate_time(k, spatial_args, time_args)
        else:
            if np.any(arg_dims[:-1]):
                return self._interpolate_array(k, spatial_args, time_args)
            else:
                return self._interpolate_scalar(k, spatial_args, time_args)

    def __getitem__(self, k):

        def property_interp(*xargs):
            return self.__call__(k, *xargs)

        return property_interp

    def __iter__(self):
        self.iterator_keys = sorted(list(self.properties.keys()))
        self.iterator_step = 0
        return self

    def __next__(self):
        if self.iterator_step < len(self.iterator_keys):
            k = self.iterator_keys[self.iterator_step]
            self.iterator_step += 1
            return k, self.__getitem__(k)
        else:
            raise StopIteration

    def keys(self):
        return self.properties.keys()

    def items(self):
        return self.__iter__()
