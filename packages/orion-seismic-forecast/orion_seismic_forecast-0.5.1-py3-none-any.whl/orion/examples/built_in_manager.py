# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import os
import glob
import json
import re
import requests
import logging
from zipfile import ZipFile
import multiprocessing
from functools import partial
from tqdm.auto import tqdm
import pathlib
import shutil
import tempfile

_path_checks = [
    'SeismicCatalog/catalog_source', 'PressureManager/PretrainedMLModel/model_path',
    'PressureManager/PressureTableModel/file_name', 'WellManager/*/fname', 'GeologicModelManager/permeability_file',
    'GeologicModelManager/sigma_file'
]

_path_replace_string = '[BUILT_IN_PATH]'


def file_download_progress(headers, url, filename):
    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    if r.status_code != 200:
        r.raise_for_status()
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")

    file_size = int(r.headers.get('Content-Length', 0))
    desc = "(Unknown total file size)" if file_size == 0 else ""

    try:
        r.raw.read = partial(r.raw.read, decode_content=True)
        with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)

    except:
        with path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)


def download_extract_zip_file(headers, path, url):
    """Download and extract a zip file

    Args:
        headers (dict): Headers for the request
        path (str): The path to extract the data
        url (str): The url for the request

    Returns
        int: an flag to indicate if there were any errors
    """
    error_flag = 0
    zip_path = os.path.join(path, 'download', 'download.zip')

    try:
        file_download_progress(headers, url, zip_path)
        zipfile = ZipFile(zip_path)
        zipfile.extractall(path)
    except Exception as e:
        logger = logging.getLogger('orion_logger')
        logger.error(e)
        error_flag = 1

    shutil.rmtree(zip_path, ignore_errors=True)
    return error_flag


class RemoteExampleManager():
    """
    Manages remote examples hosted on EDX

    Attributes:
        cache_root (str): The orion cache directory
        cache_file (str): The example downloads cache file
        edx_url (str): The expected format for EDX downloads
        available_examples (dict): A dictionary of example names and EDX resource ID numbers
        edx_api_key (str): The user's EDX API key
        download_path (str): The target download path for examples
        force_examples (int): A flag to indicate whether to override existing examples (0=ignore)
    """

    def __init__(self):
        self.cache_root = os.path.expanduser('~/.cache/orion')
        self.cache_file = os.path.join(self.cache_root, 'example_downloads.json')

        self.edx_url = 'https://edx.netl.doe.gov/resource/{}/download'
        self.available_examples = {
            'Decatur': 'efe55ae3-0425-4649-8237-8fd06a0868d3',
            'California': 'bdc866dd-55c7-4f13-83dc-b82492742db1',
            'Oklahoma': '832c9b35-52ce-48f0-8eef-6e256c5b61e7',
            'Texas': '1141a32a-9eb6-440b-84f2-076069b60806',
        }

        self.edx_api_key = ''
        self.edx_api_regex = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        self.edx_api_help_url = 'https://edx.netl.doe.gov/edxapidocs/obtainingAPIKey.html'

        self.download_path = os.path.join(self.cache_root, 'examples')

        self.current_examples = []
        self.download_examples = []
        self.force_download = 0

        self.logger = logging.getLogger('orion_logger')
        self.check_cache()
        self.check_data()

    def check_cache(self):
        """
        Check for and load the cached configuration values
        """
        if os.path.isfile(self.cache_file):
            with open(self.cache_file, 'r') as f:
                config = json.load(f)
                self.edx_api_key = config['edx_api_key']
                self.download_path = config['download_path']
                self.force_download = config['force_download']
        else:
            self.save_cache()

    def save_cache(self):
        """
        Save the current configuration to the orion cache directory

        Note: this may contain the user's EDX API key, so it is separate from the main cache file.
        In general, this data should not be shared with others.
        """
        os.makedirs(self.cache_root, exist_ok=True)
        config = {
            'edx_api_key': self.edx_api_key,
            'download_path': self.download_path,
            'force_download': self.force_download
        }
        with open(self.cache_file, 'w') as f:
            json.dump(config, f, indent=4)

    def check_data(self):
        """
        Check for existing examples on the local device
        """
        p = os.path.expanduser(self.download_path)
        self.current_examples = []
        if os.path.isdir(p):
            for k in os.listdir(p):
                if k in self.available_examples:
                    self.current_examples.append(k)

    def download_data(self, status=None):
        """
        Download the selected data to the local device.

        Args:
            status (ttk.StringVar): Handle of status variable
        """

        def set_status(label):
            if status:
                status.set(label)

        if not re.fullmatch(self.edx_api_regex, self.edx_api_key):
            self.logger.error(f'The supplied EDX API key ({self.edx_api_key}) does not appear to be valid')
            self.logger.error('Please see the following link for details on obtaining this:')
            self.logger.error('https://edx.netl.doe.gov/edxapidocs/obtainingAPIKey.html')
            return

        edx_headers = {"EDX-API-Key": self.edx_api_key, 'User-Agent': 'Mozilla/5.0'}

        self.check_data()
        self.logger.info('Checking data download requests')
        p = os.path.expanduser(self.download_path)
        os.makedirs(p, exist_ok=True)
        download_fn = partial(download_extract_zip_file, edx_headers, p)

        for k in self.download_examples:
            if (k not in self.current_examples) | self.force_download:
                self.logger.info(f'Downloading example: {k}')
                set_status(k)
                resource_url = self.edx_url.format(self.available_examples[k])
                pool = multiprocessing.Pool(processes=1)
                download_results = pool.map(download_fn, [resource_url])
                pool.close()
                pool.join()
                if download_results[0]:
                    self.logger.error('Download failed... Please check your EDX API Key and/or EDX status')

        self.logger.info('Data requests complete!')
        self.check_data()
        self.save_cache()
        set_status('')


remote_examples = RemoteExampleManager()


def find_built_in_files():
    """
    Find built in file locations, variant names
    """
    available_sources = {}
    for p in [remote_examples.download_path]:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            built_in = sorted(os.listdir(p))
            for f in built_in:
                f_full = os.path.abspath(os.path.join(p, f))
                for ka in glob.glob(f'{f_full}/config*.json'):
                    config_fname = os.path.split(ka)[1]
                    variant_id = config_fname[6:-5]
                    if len(variant_id):
                        available_sources[f + variant_id] = {'base_id': f, 'variant_id': variant_id, 'root': f_full}
                    else:
                        available_sources[f] = {'base_id': f, 'variant_id': '', 'root': f_full}

    return available_sources


def compile_built_in(case_name, target_config):
    """
    Compiles a built-in configuration file for the local machine

    Args:
        case_name (str): Name of built in case
        target_config (str): Location to place file
    """
    available_sources = find_built_in_files()
    if (case_name in available_sources):
        built_in_path = available_sources[case_name]['root']
        with open(os.path.join(built_in_path, f"config{available_sources[case_name]['variant_id']}.json")) as f:
            # Update the paths
            values = f.read()
            built_in_path = built_in_path.replace('\\', '\\\\')
            values = values.replace(_path_replace_string, built_in_path)
            with open(target_config, 'w') as g:
                g.write(values)
    else:
        print(f'Built in config not found for: {case_name}')


def config_convert_pack_files_recursive(target, config, pack_dir):
    if isinstance(target, list):
        for k in target:
            config_convert_pack_files_recursive(k, config, pack_dir)
    else:
        tmp = target.split('/')
        k = tmp[0]
        if (len(tmp) > 1):
            kb = '/'.join(tmp[1:])
            target_children = [k]
            if (k == '*'):
                target_children = list(config.keys())

            for kc in target_children:
                if kc in config:
                    child = config[kc]
                    if isinstance(child, dict):
                        config_convert_pack_files_recursive(kb, child, pack_dir)

        elif k in config:
            if config[k]:
                file_root, file_name = os.path.split(config[k])
                shutil.copy2(config[k], os.path.join(pack_dir, file_name))
                config[k] = os.path.join(_path_replace_string, file_name)


def convert_config_to_example(zip_fname, json_fname):
    logger = logging.getLogger('orion_logger')

    # Setup directory structure
    logger.info('Converting config json file to example zip')
    root, zip_name = os.path.split(zip_fname)
    zip_header = zip_name[:zip_name.rfind('.')]
    tmp_dir = tempfile.mkdtemp()
    pack_dir = os.path.join(tmp_dir, zip_header)
    new_json_fname = os.path.join(pack_dir, 'config.json')
    os.makedirs(pack_dir)

    # Load and process the config file
    config = json.load(open(json_fname, 'r'))
    if ('log_file' in config):
        del config['log_file']

    logger.debug('Copying any files present in the config...')
    config_convert_pack_files_recursive(_path_checks, config, pack_dir)
    with open(new_json_fname, 'w') as f:
        json.dump(config, f, indent=4)

    # Zip the examples
    logger.debug('Compressing the example...')
    f = zip_fname[:zip_fname.rfind('.')]
    shutil.make_archive(f, 'zip', tmp_dir)
    shutil.rmtree(tmp_dir)
    logger.debug('Done!')
