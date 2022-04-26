import sys
import json
import logging

import jinja2

from app.keycode_mapper import map_key

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

LAYOUT_NAME = "LAYOUT_splitRS"
UNICODE_INPUT_MODE = "UC_LNX"
EXPECTED_NB_KEYS = [15, 14, 13, 13, 11]


def main():
    with open("static/layers.json", "r") as f:
        layers = json.load(f)

    transformed_layers = []
    for layer_name, layer_info in layers.items():
        for shift_layer in [False, True]:
            layer_name = (
                layer_name if not shift_layer else f"{layer_name}_SHIFT"
            )

            logger.info(f"Converting layer {layer_name}")
            transformed_layer = {"name": layer_name, "separator": ","}
            rows = convert_layer(
                layer=layer_info["layout"],
                layer_name=layer_name,
                shift_layer=shift_layer,
            )

            keys = ""
            for row, expected_nb_key in zip(rows, EXPECTED_NB_KEYS):
                assert len(row) == expected_nb_key

                keys += ("\t" * 3) + (
                    ",".join([f"{keycode: <14}" for keycode in row])
                    + ","
                    + "\n"
                )
            keys = keys[:-2]  # Removing the last line break & comma
            transformed_layer["keys"] = keys
            transformed_layers.append(transformed_layer)

    transformed_layers[-1]["separator"] = ""
    with open("static/template_layout.j2", "r") as f:
        template = jinja2.Template(f.read())
    with open("keymap.c", "w") as f:
        f.write(
            template.render(
                layout_name=LAYOUT_NAME,
                layers=transformed_layers,
                unicode_input_mode=UNICODE_INPUT_MODE,
                magic_key="MAGIC_KEY",
                magic_key_layer_hold="OTHER",
                magic_key_layer_tap="AZERTY",
            )
        )


def convert_layer(layer, layer_name=None, shift_layer=False):
    converted_rows = []
    for row in layer:
        converted_row = []
        for char in row:
            if not isinstance(char, str):
                continue
            converted_row.append(
                map_key(char, layer_name=layer_name, is_shift=shift_layer)
            )
        converted_rows.append(converted_row)
    return converted_rows


if __name__ == "__main__":
    main()
