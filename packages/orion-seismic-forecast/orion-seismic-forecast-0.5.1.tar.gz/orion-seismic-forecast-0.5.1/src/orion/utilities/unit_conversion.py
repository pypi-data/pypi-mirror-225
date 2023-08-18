# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
unit_conversion.py
-----------------------
"""

import re
import logging


class DictRegexHandler():
    """This class is used to substitute matched values with those stored in a dict."""

    def __init__(self):
        """Initialize the handler with an empty target list.
           The key/value pairs of self.target indicate which values
           to look for and the values they will replace with.
        """
        self.target = {}

    def __call__(self, match):
        """Replace the matching strings with their target.
           @param match A matching string identified by the regex.
        """

        k = match.group(1)
        if k:
            if (k not in self.target.keys()):
                raise Exception(f'Error: Target ({k}) is not defined in the regex handler')
            value = self.target[k]
            return str(value)
        else:
            return


class UnitManager():
    """This class is used to manage unit definitions."""

    def __init__(self):
        """Initialize the class by creating an instance of the dict regex handler, building units."""
        self.units = {}
        self.unit_pattern = r"([a-zA-Z]*)"
        self.sanitize_pattern = r"[a-z-[e]A-Z-[E]]"
        self.logger = logging.getLogger('orion_logger')
        self.unitMatcher = DictRegexHandler()
        self.buildUnits()

    def __call__(self, unit):
        """Evaluate the symbolic expression for matched strings.

           @param unit A list containing the variable scale and the unit definition.
        """
        self.logger.debug(f'Converting units: {unit}')

        # Replace all instances of units in the string with their scale defined in self.units
        symbolicUnits = re.sub(self.unit_pattern, self.unitMatcher, unit)

        # Strip out any undesired characters and evaluate
        symbolicUnits_sanitized = re.sub(self.sanitize_pattern, '', symbolicUnits).strip()
        value = eval(symbolicUnits_sanitized, {'__builtins__': None})
        return value

    def regexHandler(self, match):
        """Split the matched string into a scale and unit definition.

           @param match The matching string from the regex.
        """
        # The first matched group includes the scale of the value (e.g. 1.234)
        # The second matches the string inside the unit definition (e.g. m/s**2)
        return self.__call__([match.group(1), match.group(2)])

    def buildUnits(self):
        """Build the unit definitions."""

        # Long, short names for SI prefixes
        # yapf: disable
        prefixes = {'giga':  {'value': 1e9,  'alt': 'G'},
                    'mega':  {'value': 1e6,  'alt': 'M'},
                    'kilo':  {'value': 1e3,  'alt': 'k'},
                    'hecto': {'value': 1e2,  'alt': 'H'},
                    'deca':  {'value': 1e1,  'alt': 'D'},
                    '':      {'value': 1.0,  'alt': ''},
                    'deci':  {'value': 1e-1, 'alt': 'd'},
                    'centi': {'value': 1e-2, 'alt': 'c'},
                    'milli': {'value': 1e-3, 'alt': 'm'},
                    'micro': {'value': 1e-6, 'alt': 'mu'},
                    'nano':  {'value': 1e-9, 'alt': 'n'}}

        # Base units, and their abbreviations
        # Note: setting (usePrefix = True) instructs the manager to expand using SI prefixes
        unit_defs = {'gram':   {'value': 1e-3,               'alt': ['g', 'grams'],         'usePrefix': True},
                     'meter':  {'value': 1.0,                'alt': ['m', 'meters'],        'usePrefix': True},
                     'second': {'value': 1.0,                'alt': ['s', 'seconds'],       'usePrefix': True},
                     'minute': {'value': 60.0,               'alt': ['min', 'minutes'],     'usePrefix': True},
                     'hour':   {'value': 3600.0,             'alt': ['hr', 'hours', 'hrs'], 'usePrefix': True},
                     'day':    {'value': 3600.0*24.0,        'alt': ['d', 'dy'],            'usePrefix': True},
                     'year':   {'value': 3600.0*24.0*365.25, 'alt': ['yr', 'years'],        'usePrefix': True},
                     'pascal': {'value': 1.0,                'alt': ['Pa'],                 'usePrefix': True},
                     'newton': {'value': 1.0,                'alt': ['N'],                  'usePrefix': True},
                     'joule':  {'value': 1.0,                'alt': ['J'],                  'usePrefix': True},
                     'watt':   {'value': 1.0,                'alt': ['W'],                  'usePrefix': True}}

        # Imperial units, and their abbreviations
        imp_defs = {'pound':      {'value': 0.453592,       'alt': ['lb', 'pounds', 'lbs'], 'usePrefix': True},
                    'poundforce': {'value': 0.453592*9.81,  'alt': ['lbf'],                 'usePrefix': True},
                    'stone':      {'value': 6.35029,        'alt': ['st'],                  'usePrefix': True},
                    'ton':        {'value': 907.185,        'alt': ['tons'],                'usePrefix': True},
                    'inch':       {'value': 1.0/(3.281*12), 'alt': ['in', 'inches'],        'usePrefix': False},
                    'foot':       {'value': 1.0/3.281,      'alt': ['ft', 'feet'],          'usePrefix': True},
                    'yard':       {'value': 3.0/3.281,      'alt': ['yd', 'yards'],         'usePrefix': True},
                    'rod':        {'value': 16.5/3.281,     'alt': ['rd', 'rods'],          'usePrefix': True},
                    'mile':       {'value': 5280.0/3.281,   'alt': ['mi', 'miles'],         'usePrefix': True},
                    'acre':       {'value': 4046.86,        'alt': ['acres'],               'usePrefix': True},
                    'gallon':     {'value': 0.00378541,     'alt': ['gal', 'gallons'],      'usePrefix': True},
                    'psi':        {'value': 6894.76,        'alt': [],                      'usePrefix': True},
                    'psf':        {'value': 1853.184,       'alt': [],                      'usePrefix': True}}

        # Other commonly used units:
        other_defs = {'dyne':       {'value': 1.0e-5,    'alt': ['dynes'],              'usePrefix': True},
                      'bar':        {'value': 1.0e5,     'alt': ['bars'],               'usePrefix': True},
                      'atmosphere': {'value': 101325.0,  'alt': ['atm', 'atmospheres'], 'usePrefix': True},
                      'poise':      {'value': 0.1,       'alt': ['P'],                  'usePrefix': True},
                      'barrel':     {'value': 0.1589873, 'alt': ['bbl', 'barrels'],     'usePrefix': True},
                      'horsepower': {'value': 745.7,     'alt': ['hp', 'horsepowers'],  'usePrefix': True}}

        # Combine the unit dicts
        # yapf: enable
        unit_defs.update(imp_defs)
        unit_defs.update(other_defs)

        # Use brute-force to generate a list of potential units, rather than trying to parse
        # unit strings on the fly.  This is still quite fast, and allows us to do simple
        # checks for overlapping definitions

        # Expand prefix and alternate names
        for p in list(prefixes.keys()):
            if prefixes[p]['alt']:
                prefixes[prefixes[p]['alt']] = {'value': prefixes[p]['value']}
        for u in list(unit_defs.keys()):
            for alt in unit_defs[u]['alt']:
                unit_defs[alt] = {'value': unit_defs[u]['value'], 'usePrefix': unit_defs[u]['usePrefix']}

        # Combine the results into the final dictionary
        for u in unit_defs.keys():
            if (unit_defs[u]['usePrefix']):
                for p in prefixes.keys():
                    self.units[p + u] = prefixes[p]['value'] * unit_defs[u]['value']
            else:
                self.units[u] = unit_defs[u]['value']

        # Test to make sure that there are no overlapping unit definitions
        from collections import Counter
        tmp = list(self.units.keys())
        duplicates = [k for k, v in Counter(tmp).items() if v > 1]
        if (duplicates):
            self.logger.error(duplicates)
            raise Exception('Error: There are overlapping unit definitions in the UnitManager')

        self.unitMatcher.target = self.units
