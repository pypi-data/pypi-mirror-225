# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
wizard_base.py
--------------------------------------
"""

from tkinter import ttk, filedialog
from orion.gui.gui_base import GUIBase, set_relative_size
from orion.gui.gui_element_factory import add_element, element_variable_map
import logging


class WizardStepBase():
    """
    Wizard Step Base Class
    """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent.wizard_container)
        self.logger = parent.logger
        self.step_label = ''
        self.step_status = ''

    def grid(self):
        self.frame.grid(sticky='news')

    def grid_forget(self):
        self.frame.grid_forget()

    def destroy(self):
        self.frame.grid_forget()
        self.frame.destroy()

    def create_all(self):
        self.create_step()
        self.create_main()

    def create_step(self):
        """
        Create step elements
        """
        pass

    def create_main(self):
        """
        Add elements to the step frame
        """
        if self.step_label:
            step_label = ttk.Label(self.frame, text=self.step_label)
            step_label.grid(row=0, column=0, columnspan=10, padx=5, pady=5, sticky='new')
        self.grid()

    def step_forward(self):
        """
        Step forward to the next wizard step
        """
        pass

    def finalize_step(self):
        """
        Finalize the step.
        Any subsequent steps should be added to the queue here
        """
        pass


class WizardBase(GUIBase):
    """
    Wizard base class
    """

    def __init__(self, parent, gui_name='wizard'):
        """
        Orion information gui initialization
        """
        # Call the parent's initialization
        super().__init__(parent.child_gui[gui_name]['window'])
        self.gui_name = gui_name

        self.logger = logging.getLogger('orion_logger')

        # Wizard objects
        self.parent = parent
        self.wizard_container = None
        self.wizard_first_step_class = None
        self.wizard_steps = []
        self.wizard_step_queue = []
        self.step_queue_history = [[]]

        # Setup the container
        self.set_icon()

    def quit(self):
        """
        Close the config gui
        """
        self.window.withdraw()
        self.window.destroy()
        del self.parent.child_gui[self.gui_name]

    def queue_steps(self, step_type):
        if isinstance(step_type, list):
            self.wizard_step_queue.extend(step_type)
        else:
            self.wizard_step_queue.append(step_type)

    def create_main(self):
        """
        Create the config gui main page
        """
        # Create the main window
        self.frame.pack(fill='both', expand=True)
        self.window.title(self.gui_name)
        self.window.protocol('WM_DELETE_WINDOW', self.quit)
        self.wizard_container = ttk.Frame(self.frame)
        self.wizard_container.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='news')

        # Status
        status_label = ttk.Label(self.frame, textvariable=self.status_label)
        status_label.grid(row=1, column=1, padx=5, pady=5, sticky='ne')

        # Request
        back_button = ttk.Button(self.frame, text='Previous', width=self.button_width, command=self.wizard_step_back)
        back_button.grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        forward_button = ttk.Button(self.frame, text='Next', width=self.button_width, command=self.wizard_step_forward)
        forward_button.grid(row=2, column=1, padx=5, pady=5, sticky='ne')

        # Finalize objects
        set_relative_size(self.frame)
        self.frame.grid_rowconfigure(1, weight=0)

        # Add the first step
        if self.wizard_first_step_class is not None:
            self.wizard_steps.append(self.wizard_first_step_class(self))
            self.wizard_steps[0].create_all()
        else:
            self.logger.error('This wizard does not have any steps!')
            self.quit()

    def wizard_step_back(self):
        """
        Move backwards through the wizard
        """
        if len(self.wizard_steps) > 1:
            # Return to a previous step
            self.logger.debug('Returning to the previous wizard step')
            self.wizard_steps[-1].destroy()
            del self.wizard_steps[-1]
            self.wizard_steps[-1].grid()

            # Rewind the queue
            del self.step_queue_history[-1]
            self.wizard_step_queue = self.step_queue_history[-1].copy()
        else:
            self.logger.debug('You have reached the start of the wizard and cannot step back further')

    def wizard_step_forward(self):
        """
        Move forward through the wizard
        """
        # Test moving forward:
        err = self.wizard_steps[-1].step_forward()
        if err:
            self.logger.debug('Staying on the current step')
            return

        next_step_class = None
        if len(self.wizard_step_queue):
            next_step_class = self.wizard_step_queue.pop(0)

        self.step_queue_history.append(self.wizard_step_queue.copy())

        # Otherwise clear the current step and move on the the next if defined
        self.wizard_steps[-1].grid_forget()
        if next_step_class is not None:
            self.logger.debug('Moving forward to the next wizard step')
            self.wizard_steps.append(next_step_class(self))
            self.wizard_steps[-1].create_all()
        else:
            self.logger.debug('You have reached the end of the wizard')
            self.wizard_finalize()
            self.quit()

    def wizard_finalize(self):
        pass


def set_variable_from_dialogue_factory(var, filetypes):

    def set_variable_from_dialogue():
        if 'folder' in filetypes:
            var.set(filedialog.askdirectory())
        else:
            var.set(filedialog.askopenfilename(filetypes=filetypes))

    return set_variable_from_dialogue


class OrionWizardStepBase(WizardStepBase):
    """
    Wizard Step Base Class
    """

    def __init__(self, parent):
        super().__init__(parent)
        # self.children = {}
        self.wizard_elements = {}
        self.variables = {}

    def function_helper(self, parent, config, target_fn, filetypes=[], target_arg_names=[], pre_update=False):
        """
        Runs a function when a button is pressed.

        Args:
            parent (orion.managers.orion_manager.OrionManager) object to check for changes
            target_fn: Target function to run
            filetypes (list): List of file filters
        """
        if (self.enable_callbacks & pre_update):
            self.update_config()

        target_args = [self.parent.orion_manager.children[k] for k in target_arg_names]
        if len(filetypes):
            if 'folder' in filetypes:
                target_fn(filedialog.askdirectory(), *target_args)
            else:
                target_fn(filedialog.askopenfilename(filetypes=filetypes), *target_args)
        else:
            target_fn(*target_args)

        if self.enable_callbacks:
            self.check_gui_children()

    def create_all(self):
        super().create_all()
        for k, x in self.wizard_elements.items():
            parent = x['parent']
            element = {}
            if hasattr(parent, 'gui_elements'):
                element = parent.gui_elements.get(k, {}).copy()
            element.update(x['config'])
            var = element_variable_map[element['element_type']]
            if var is not None:
                self.variables[k] = var()
                element['variable'] = self.variables[k]

            command = element.get('command', None)
            filetypes = element.get('filetypes', [])
            if (command == 'file'):
                element['callback'] = set_variable_from_dialogue_factory(element['variable'], filetypes)

            add_element(self.frame, parent, k, **element)

        self.set_wizard_values_from_config()

    def set_wizard_values_from_config(self):
        for ka, x in self.wizard_elements.items():
            parent = x['parent']
            current_state = getattr(parent, ka)
            self.variables[ka].set(current_state)

    def set_config_values_from_wizard(self):
        for ka, x in self.wizard_elements.items():
            parent = x['parent']

            # Handle value conversion
            current_state = ''
            if isinstance(getattr(parent, ka), str):
                current_state = self.variables[ka].get()
            elif isinstance(getattr(parent, ka), float):
                current_state = float(self.variables[ka].get())
            elif isinstance(getattr(parent, ka), int):
                current_state = int(self.variables[ka].get())
            else:
                current_state = self.variables[ka].get()
            setattr(parent, ka, current_state)

    def step_forward(self):
        self.set_config_values_from_wizard()
        return self.finalize_step()
