import json
from orion.gui.gui_element_factory import element_variable_map

# yapf: disable

# Define object options
grid_kwargs = {
    "position": {
        "type": "array",
        "items": {"type": "integer"},
        "minItems": 2,
        "maxItems": 2,
        "description": "Position of the object in the global grid (row, col)",
        "required": True
    },
    "columnspan": {
        "type": "integer",
        "description": "Span this many columns in the grid",
        "default": 1
    },
    "rowspan": {
        "type": "integer",
        "description": "Span this many rows in the grid",
        "default": 1
    },
    "units_span": {
        "type": "integer",
        "description": "Unit objects span this many rows in the grid",
        "default": 1
    }
}


figure_kwargs = {
    "size": {
        "type": "array",
        "items": {"type": "integer"},
        "minItems": 2,
        "maxItems": 2,
        "description": "Size of the figure in inches (width, height)",
        "required": True
    },
    "extra_axis_size": {
        "type": "array",
        "items": {"type": "integer"},
        "minItems": 2,
        "maxItems": 2,
        "description": "If set, place an extra axis to the right of the figure, with a given size in inches (width, height)"
    },
    "layer_config": {
        "type": "boolean",
        "description": "If set, add layer controls to the right of the figure",
        "default": False
    },
    "static": {
        "type": "boolean",
        "description": "If set, do not add a navigation bar",
        "default": False
    }
}


type_str = "|".join(sorted(list(element_variable_map.keys())))

element_kwargs = {
    "element_type": {
        "type": "string",
        "description": "Element type",
        "pattern": f"({type_str})",
        "required": True
    },
    "label": {
        "type": "string",
        "description": "Label to place to the left of the element",
        "default": ""
    },
    "units": {
        "type": "string",
        "description": "Label to place to the right of the element",
        "default": ""
    }
}


update_options = ["none", "all", "frame"]
update_str = "|".join(update_options)

button_kwargs = {
    "command": {
        "type": "string",
        "description": "Execute this command when the user interacts with the element.  This can be a function name or: file, add child, remove child",
        "default": ""
    },
    "filetypes": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Before a command is executed, open a file dialogue targeting these types (the result is passed as the first argument to the fn).",
        "default": []
    },
    "text": {
        "type": "string",
        "description": "Optional button text",
        "default": "Unnamed button"
    },
    "pre_update": {
        "type": "string",
        "description": "Update the config before executing the command",
        "pattern": f"({update_str})",
        "default": "none"
    },
    "post_update": {
        "type": "string",
        "description": "Update the config after executing the command",
        "pattern": f"({update_str})",
        "default": "none"
    }
}


dropdown_kwargs = {
    "values": {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 1,
        "description": "Options to include in a dropdown element"
    }
}


checkbox_kwargs = {
    "ncol": {
        "type": "integer",
        "description": "Number of columns to use for the checkbox element",
        "default": 1
    },
    "header": {
        "type": "string",
        "description": "Header to place at the top of the checkbox element",
        "default": ""
    },
}


gui_api = {
    "id": "manager",
    "type": "object",
    "properties": {
        "type": {"type": "object"},
        "description": {"type": "string"},
        "properties": {
            "type": "object",
            "patternProperties": {
                "[A-Za-z0-9]": {"$ref": "arg"}
            }
        }
    }
}


# Combine options
figure_options = {}
for f in [figure_kwargs, grid_kwargs]:
    figure_options.update(f)

element_options = {}
for e in [element_kwargs, button_kwargs, dropdown_kwargs, checkbox_kwargs, grid_kwargs]:
    element_options.update(e)


# Create the schema
figure_type = {
    "type": "object",
    "patternProperties": {
        "[A-Za-z0-9]": {"type": "object",
                        "properties": figure_options}
    }
}


element_type = {
    "type": "object",
    "patternProperties": {
        "[A-Za-z0-9]": {"type": "object",
                        "properties": element_options}
    }
}


children_type = {
    "type": "object",
    "patternProperties": {
        "[A-Za-z0-9]": {"$ref": "manager"}
    }
}


gui_api = {
    "$id": "manager",
    "type": "object",
    "properties": {
        "figures": figure_type,
        "gui_elements": element_type,
        "children": children_type
    }
}

# yapf: enable


def write_schema(fname):
    with open(fname, "w") as f:
        json.dump(gui_api, f, indent=4)
