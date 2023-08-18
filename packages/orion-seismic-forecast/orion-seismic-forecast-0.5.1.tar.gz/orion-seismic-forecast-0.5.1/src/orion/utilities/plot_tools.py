# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
plot_tools.py
-----------------------
"""

import numpy as np
import matplotlib as mpl
from matplotlib import cm
import matplotlib.colors as mcolors
import logging
import PIL
import contextily as cx
import requests
import urllib3

# Config
# colors = ('blue', 'cyan', 'green', 'violet', 'red', 'magenta', 'orange', 'yellow')
colors = ('foreground_0', 'blue', 'green', 'violet', 'red', 'magenta', 'orange', 'yellow')

monokai = {
    'background_0': '#272822',
    'background_1': '#3e3d32',
    'background_2': '#75715e',
    'foreground_1': '#cfcfc2',
    'foreground_0': '#f8f8f2',
    'yellow': '#e6db74',
    'orange': '#fd971f',
    'red': '#f92672',
    'magenta': '#fd5ff0',
    'violet': '#ae81ff',
    'blue': '#66d9ef',
    'cyan': '#a1efe4',
    'green': '#a6e22e'
}

monokai_ordered = [monokai[k] for k in colors]

light = {
    'background_0': '#eeeeee',
    'background_1': '#f5f5f5',
    'background_2': '#fafafa',
    'foreground_1': '#424242',
    'foreground_0': '#212121',
    'yellow': '#e6db74',
    'orange': '#fd971f',
    'red': '#f92672',
    'magenta': '#fd5ff0',
    'violet': '#ae81ff',
    'blue': '#66d9ef',
    'cyan': '#a1efe4',
    'green': '#a6e22e'
}

light_ordered = [light[k] for k in colors]

stark = {
    'background_0': '#ffffff',
    'background_1': '#ffffff',
    'background_2': '#ffffff',
    'foreground_1': '#000000',
    'foreground_0': '#000000',
    'yellow': '#fdff00',
    'orange': '#ff5f00',
    'red': '#ff0000',
    'magenta': '#ff1dce',
    'violet': '#9600ff',
    'blue': '#0000ff',
    'cyan': '#00ffff',
    'green': '#09ff00'
}

stark_ordered = [stark[k] for k in colors]

monokai_sv = {k: v for k, v in monokai.items()}
monokai_sv.update({'background_1': '#1c1c1c'})
monokai_sv_ordered = [monokai_sv[k] for k in colors]

light_sv = {k: v for k, v in light.items()}
light_sv.update({'background_1': '#fafafa'})
light_sv_ordered = [light_sv[k] for k in colors]


def exceedance_bar_plot(ax, magnitude, probability, color_lims=[0.3, 0.6]):
    """
    Build a magnitude exceedance bar plot

    Args:
        ax (matplotlib.pyplot.axis): Target figure axis
        magnitude (np.ndarray): magnitude magnitudes
        probability (np.ndarray): Probability of exceedance
        color_lims (list): Locations to place the transition between green/yellow and yellow/red
    """
    # Setup the bar color
    bar_color = []
    for p in probability:
        if (p < color_lims[0]):
            bar_color.append('g')
        elif (p < color_lims[1]):
            bar_color.append('#FFBF00')
        else:
            bar_color.append('r')

    # Set probabilities to a minimum value to ensure visibility
    probability_percent = probability
    probability_percent[probability_percent < 1.0] = 1.0

    # Build the plot
    ax.barh(magnitude, probability_percent, color=bar_color, edgecolor='k')
    ax.set_xlabel('Probability (%)')
    ax.set_ylabel('Magnitude')
    # ax.set_xlim([0.0, max(1.1 * np.amax(probability), 0.1) * 100.0])
    ax.set_xlim([0.0, 100.0])
    ax.invert_yaxis()


def exceedance_dial_plot(ax, probability, color_lims=[0.3, 0.6], ra=0.8, rb=0.9, rc=1.0):
    """
    Build a magnitude exceedance bar plot

    Args:
        ax (matplotlib.pyplot.axis): Target figure axis
        probability (np.ndarray): Probability of exceedance
        color_lims (list): Locations to place the transition between green/yellow and yellow/red
        ra (float): Radius of the pointer
        ra (float): Radius of the inner-dial
        rc (float): Radius of the outer-dial
    """
    # Draw the dial edges
    theta = np.linspace(0, 1, 100)
    x = -rb * np.cos(theta * np.pi)
    y = rb * np.sin(theta * np.pi)
    ax.plot(x, y, 'k')
    ax.plot([-rb, rb], [0, 0], 'k')

    # Draw the dial color
    dial_regions = {
        'g': [0.0, color_lims[0] * 0.01],
        '#FFBF00': [color_lims[0] * 0.01, color_lims[1] * 0.01],
        'r': [color_lims[1] * 0.01, 1.0]
    }

    for k in dial_regions:
        tmp = np.linspace(dial_regions[k][0], dial_regions[k][1], 100)
        theta = np.concatenate([tmp, tmp[::-1], [tmp[0]]], axis=0)
        radius = np.concatenate([np.zeros(len(tmp)) + ra, np.zeros(len(tmp)) + rb, [ra]], axis=0)
        x = -radius * np.cos(theta * np.pi)
        y = radius * np.sin(theta * np.pi)
        ax.fill(x, y, k)

    # Draw the labels
    ticks = np.linspace(0, 1, 11)
    for t in ticks:
        x = -rc * np.cos(t * np.pi)
        y = rc * np.sin(t * np.pi)
        ax.text(x, y, f'{int(t * 100.0)}', horizontalalignment='center', verticalalignment='top')

    # Draw the arrow
    dx = -ra * np.cos(probability * np.pi / 100.0)
    dy = ra * np.sin(probability * np.pi / 100.0)
    ax.arrow(0, 0, dx, dy, color='k', width=0.025, length_includes_head=True)

    # Configure the axis
    ax.set_xlim([-1, 1])
    ax.set_ylim([0, 1])
    ax.axis('off')


def multivariatePlot(root_axis, plots, offset_val=0.12):
    """
    Build a multivariate plot

    Args:
        root_axis (matplotlib.pyplot.axis): Target figure axis
        plots (dict): Dictionary of plot instructions
        offset_val (float): Axis offset value (default=0.12)
    """
    # Open new axes
    ax = [root_axis] + [root_axis.twinx() for p in range(1, len(plots))]

    # Render plots
    for ii in range(0, len(plots)):
        ap = plots[ii]
        if ('log' in ap.keys()):
            ax[ii].semilogy(ap['x'], ap['y'], ap['style'])
        else:
            ax[ii].plot(ap['x'], ap['y'], ap['style'])
        ax[ii].set_ylim([0.0, 1.05 * max(ap['y'])])
        ax[ii].set_ylabel(ap['ylabel'], color=ap['style'][0])

        if (ii == 0):
            ax[0].set_xlabel(ap['xlabel'])

        if (ii > 1):
            ax[ii].spines['right'].set_position(('axes', 1.0 + (ii - 1) * offset_val))
            ax[ii].set_frame_on(True)
            ax[ii].patch.set_visible(False)

        for tt in ax[ii].get_yticklabels():
            tt.set_color(ap['style'][0])

    return ax


def periodic_style(colors, lines, markers, ii):
    NC = len(colors)
    NL = len(lines)
    NM = len(markers)
    jj = ii % (NC * (NL + NM))
    kk = int(jj / NC)

    style_args = {'color': colors[jj % NC]}
    if NL:
        if (kk < NL):
            style_args['linestyle'] = lines[kk]
        else:
            style_args['marker'] = markers[(kk - NL + 1) % NM]
    else:
        style_args['linestyle'] = 'None'
        style_args['marker'] = markers[kk]

    return style_args


def registerCascadeColormap(mode='light'):
    cdict = mpl.colormaps.get_cmap('jet').__dict__['_segmentdata'].copy()
    for k in cdict.keys():
        tmp_seq = list(cdict[k])
        tmp_final = list(tmp_seq[0])
        tmp_final[1] = 1.0
        tmp_final[2] = 1.0
        if (mode == 'dark'):
            tmp_final[1] = 0.15686274509
            tmp_final[2] = 0.13333333333
        tmp_seq[0] = tuple(tmp_final)
        cdict[k] = tuple(tmp_seq)
    mpl.colormaps.unregister('cascade')
    mpl.colormaps.register(mcolors.LinearSegmentedColormap('cascade', cdict))


def registerLinearColormap(name, base_colors, N=256):
    mpl.colormaps.unregister(name)
    mpl.colormaps.register(mcolors.LinearSegmentedColormap.from_list(name, base_colors, N))


def registerStoplightColormap():
    registerLinearColormap('stoplight', ["green", "yellow", "red"])


def registerRippleColormap(mode='light'):
    colors = ['black', monokai['cyan'], monokai['green']]
    if (mode == 'dark'):
        colors[0] = monokai['foreground_0']
    registerLinearColormap('ripple', colors)


def registerUSGSHazardColormap(mode='light', N=256):
    hazard_colors = [
        'white', monokai['cyan'], monokai['green'], monokai['yellow'], monokai['orange'], monokai['red'],
        monokai['magenta']
    ]
    if (mode == 'dark'):
        hazard_colors[0] = monokai['background_0']
    registerLinearColormap('hazard', hazard_colors)


class DefaultDict():

    def __init__(self):
        self.dict = {}

    def __setitem__(self, k, value):
        self.dict[k] = value

    def __getitem__(self, k):
        if k in self.dict:
            return self.dict[k]
        else:
            return True


def getPlotVisibility(ax):
    visibility = DefaultDict()
    for child in ax.get_children():
        name = child.get_label()
        if name:
            visibility[name] = child.get_visible()
    return visibility


def formatRange(init_range, precision=1, min_range=0.1):
    scale = 10**precision
    new_min = scale * np.floor(init_range[0] / scale)
    new_max = scale * np.ceil(init_range[1] / scale)
    if (new_max - new_min < min_range):
        new_max = new_min + min_range
    return [new_min, new_max]


def setupColorbar(fig, ca, cax, value_range, label):
    """
    Setup a colorbar, optimizing the number and format of ticks

    Args:
        fig (matplotlib.figure.Figure): Target figure handle
        ca (matplotlib.image.AxesImage): AxesImage from plt.imshow
        cax (matplotlib.axes.Axes): Location to place colorbar
        value_range (list): Target value range
        label (str): Colorbar label
    """
    Nticks = max(min(5, int(value_range[1] - value_range[0])), 2)
    tick_location = np.linspace(value_range[0], value_range[1], Nticks)

    test_value = max(abs(value_range[0]), abs(value_range[1]))
    tick_order = 1
    if (test_value > 0):
        tick_order = int(np.ceil(np.log10(test_value)))

    tick_format = '%i'
    if (abs(tick_order) > 4):
        tick_format = '%1.1e'
    elif (tick_order < 0):
        tick_format = f'%1.{-tick_order}f'
    cb = fig.colorbar(ca, cax=cax, format=tick_format, ticks=tick_location)
    cb.set_label(label)


def add_basemap(*xargs, **kwargs):
    # Check inputs
    if ('source' not in kwargs):
        kwargs['source'] = cx.providers.Stamen.TonerLite

    if ('attribution' not in kwargs):
        kwargs['attribution'] = ''

    # Check whether to add an empty map
    add_empty_map = False
    plot_kwargs = kwargs.copy()
    if ('add_map' in kwargs):
        if not kwargs['add_map']:
            add_empty_map = True
        del plot_kwargs['add_map']

    # Add map layer or dummy placeholder
    logger = logging.getLogger('orion_logger')
    try:
        if not add_empty_map:
            cx.add_basemap(*xargs, **plot_kwargs)
            add_empty_map = False
    except PIL.UnidentifiedImageError:
        logger.warning('Map did not render... This can sometimes happen if the bounding box is too small')
        add_empty_map = True
    except requests.exceptions.SSLError:
        logger.warning('Could not fetch map imagery due to a certificate error...')
        logger.warning('This check can be overridden in the config window under Orion/Allow self-signed certs')
        add_empty_map = True
    except Exception as e:
        logger.warning('Could not fetch map imagery due to a network connectivity issue...')
        logger.warning(e)

    if add_empty_map:
        dummy = np.zeros((2, 2))
        dummy_kwargs = {k: plot_kwargs[k] for k in ['label', 'visible'] if k in plot_kwargs}
        dummy_kwargs['alpha'] = 0.0
        xargs[0].imshow(dummy, **dummy_kwargs)
