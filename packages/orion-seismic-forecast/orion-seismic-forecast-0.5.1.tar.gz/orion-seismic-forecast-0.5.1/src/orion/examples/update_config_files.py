# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import glob
import json


def compare_recursive(source_dict, target_dict):
    diffs = 0
    source_keys = list(source_dict.keys())
    target_keys = list(target_dict.keys())

    # Check for new values to add
    for k in source_keys:
        if isinstance(source_dict[k], dict):
            if (k in target_keys):
                diffs += compare_recursive(source_dict[k], target_dict[k])
            else:
                target_dict[k] = source_dict[k]
                diffs += 1
        else:
            if (k not in target_keys):
                diffs += 1
                target_dict[k] = source_dict[k]

    # Check for values to remove
    for k in target_keys:
        if (k not in source_keys):
            diffs += 1
            del target_dict[k]

    return diffs


# Config
new_config_fname = '/usr/workspace/sherman/Python/orion/orion/examples/test.json'
data_root = '.'

# Load the new config file to look for entry changes
f = open(new_config_fname, 'r')
new_config = json.load(f)
f.close()

# Compare against existing json files
for fname in glob.glob(f'{data_root}/*/config.json'):
    f = open(fname, 'r')
    target_config = json.load(f)
    f.close()

    diffs = compare_recursive(new_config, target_config)
    if (diffs > 0):
        f = open(fname, 'w')
        json.dump(target_config, f, indent=4)
        f.close()
