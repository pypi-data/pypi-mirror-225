from tkinter import ttk, IntVar, StringVar, DoubleVar
from orion.gui.custom_widgets import LabeledScale


def gui_text(frame, parent, name, element, var):
    return ttk.Label(frame, textvariable=var)


def gui_check(frame, parent, name, element, var):
    return ttk.Checkbutton(frame, variable=var)


def gui_checkbox(frame, parent, name, element, var):
    obj = ttk.Frame(frame, borderwidth=2, relief='sunken')
    if ('header' in element):
        add_element(obj, parent, 'header', element_type='text', label=element['header'], position=(0, 0))
    ncol = element.get('ncol', 2)
    target_dict = getattr(parent, name)
    if not isinstance(target_dict, dict):
        raise Exception('A GUI checkbox must target a dictionary on the current object')

    for ii, kc in enumerate(sorted(target_dict.keys())):
        row = (ii // ncol) + 1
        col = ii % ncol
        add_element(obj, parent, kc, element_type='check', variable=var[kc], label=kc, position=(row, col))
    return obj


def gui_slider(frame, parent, name, element, var):
    r = element.get('range', [0, 1])
    n = element.get('interval', 4)
    return LabeledScale(frame, scale_range=(r[0], r[1]), variable=var, length=200, Nticks=n, orient='horizontal')


def gui_dropdown(frame, parent, name, element, var):
    w = element.get('width', 20)
    return ttk.Combobox(frame, values=element['values'], textvariable=var, width=w)


def gui_entry(frame, parent, name, element, var):
    w = element.get('width', 20)
    if 'callback' in element:
        obj = ttk.Frame(frame)
        gui_text = element.get('text', ':')

        # Note: set units_span to 1 so that the child frame grids properly
        element['units_span'] = 1
        add_element(obj, parent, 'file_entry', element_type='entry', variable=var, width=w, position=(0, 1))
        add_element(obj,
                    parent,
                    'file_button',
                    element_type='button',
                    text=gui_text,
                    callback=element['callback'],
                    position=(0, 2))
        return obj
    else:
        return ttk.Entry(frame, width=w, textvariable=var)


def gui_button(frame, parent, name, element, var):
    button_text = element.get('text', 'Unnamed button')
    return ttk.Button(frame, text=button_text, width=len(button_text), command=element['callback'])


def var_none():
    return None


class CheckboxDict():

    def __init__(self):
        self._dict = {}

    def __getitem__(self, k):
        if k not in self._dict:
            self._dict[k] = IntVar()
        return self._dict[k]

    def set(self, state):
        for k, v in state.items():
            self[k].set(int(v))

    def get(self):
        return {k: int(self[k].get()) for k in self._dict.keys()}


element_type_map = {
    'text': gui_text,
    'check': gui_check,
    'checkbox': gui_checkbox,
    'slider': gui_slider,
    'dropdown': gui_dropdown,
    'entry': gui_entry,
    'button': gui_button
}

element_variable_map = {
    'text': StringVar,
    'check': IntVar,
    'checkbox': CheckboxDict,
    'slider': DoubleVar,
    'dropdown': StringVar,
    'entry': StringVar,
    'button': var_none
}


def add_element(*xargs, **kwargs):
    """
    Add an element to the gui
    """
    # Handle multiple object instances
    if isinstance(kwargs['position'][0], int):
        add_element_b(*xargs, **kwargs)
    else:
        k = kwargs.copy()
        for p in kwargs['position']:
            k['position'] = p
            add_element_b(*xargs, **k)


def add_element_b(frame, parent, name, **element):
    """
    Add gui elements to the target frame

    Args:
        frame (ttk.Frame): The target frame
        parent (orion.managers.manager_base.ManagerBase): The associated orion manager
        name (str): The name of the target variable
        element (dict): Element description
    """
    objects = []
    extra_grid_args = {}
    var = element.get('variable', None)

    # Handle labels
    if ('label' in element):
        objects.append(ttk.Label(frame, text=element['label']))

    # Handle element types
    objects.append(element_type_map[element['element_type']](frame, parent, name, element, var))

    # Handle units
    if ('units' in element):
        objects.append(ttk.Label(frame, text=element['units']))

    # Grid the elements
    N = len(objects)
    span = [1 for _ in objects]
    span[-1] = element.get('units_span', element.get('columnspan', 4 - N))
    for ii, x in enumerate(objects):
        x.grid(row=element['position'][0],
               column=3 * element['position'][1] + ii,
               sticky='nw',
               padx=5,
               pady=5,
               columnspan=span[ii],
               **extra_grid_args)
