import re
from string import ascii_uppercase


def map_key(key, is_shift=False, layer_name=None):
    key = key.lower()

    candidate = _layer_dependent_mapping(key, is_shift, layer_name)
    if candidate is not None:
        return candidate

    if "\n\n\n" in key:
        parts, kind = key.split("\n\n\n")
        assert "\n" in parts
        key = tuple([kind, *parts.split("\n")])
        return _keycode_mapper(key)

    if "\n" in key:
        parts = key.split("\n")
        key = tuple(parts)

        if _is_simple_case(key):
            return f"LSFT({_keycode_mapper(key)})" if is_shift else _keycode_mapper(key)
        key = parts[0] if is_shift else parts[1]
        keycode = _keycode_mapper(key)
        if keycode in ["KC_LEFT", "KC_RIGHT", "KC_UP", "KC_DOWN"] and is_shift:
            return f"LSFT({keycode})"
        return keycode

    return f"LSFT({_keycode_mapper(key)})" if is_shift else _keycode_mapper(key)


def _layer_dependent_mapping(key, is_shift=False, layer_name=None):
    if key in ["l-shift", "shift"] and layer_name is not None:
        if is_shift:
            return _keycode_mapper("")
        dest_layer_name = f"{layer_name}_SHIFT"
        return f"MO({dest_layer_name})"

    if key in ["esc", "hyper"]:
        return _keycode_mapper(key) if not is_shift else "KC_GRAVE"

    return None


def _get_unicode(char) -> str:
    return hex(ord(char))


def _to_lowercase(key):
    if isinstance(key, str):
        return key.lower()
    if isinstance(key, tuple):
        return tuple([_to_lowercase(part) for part in key])


def _is_simple_case(key):
    try:
        _keycode_mapper(key)
    except:
        return False
    return True


def _keycode_mapper(key):
    if key in dict_keycode_mapper:
        return dict_keycode_mapper[key]

    assert isinstance(key, str)
    pattern = "<i class='(?P<key>[a-z0-9 -]+)'></i>"
    matches = re.match(pattern, key)
    if matches:
        return dict_keycode_mapper[matches.group("key")]

    raise Exception(f"Can't find QMK conversion for {key}")


TRANSPARENT = "_______"
ENTER = "KC_ENT"
SPACE = "KC_SPC"
BACKSPACE = "KC_BSPACE"
ESCAPE = "KC_ESC"
SHIFT = "KC_LSHIFT"
VOLUME_UP = "KC_VOLU"
VOLUME_DOWN = "KC_VOLD"

dict_keycode_mapper = {
    "!": "KC_EXLM",
    "": TRANSPARENT,
    "#": "KC_HASH",
    "$": "KC_DLR",
    "%": "KC_PERC",
    "&": "KC_AMPR",
    "'": "KC_QUOTE",
    "(": "KC_LPRN",
    ")": "KC_RPRN",
    "*": "KC_ASTR",
    "+": "KC_PLUS",
    ",": "KC_COMMA",
    "-": "KC_MINUS",
    ".": "KC_DOT",
    "/": "KC_SLASH",
    "0": "KC_0",
    "1": "KC_1",
    "2": "KC_2",
    "3": "KC_3",
    "4": "KC_4",
    "5": "KC_5",
    "6": "KC_6",
    "7": "KC_7",
    "8": "KC_8",
    "9": "KC_9",
    ":": "KC_COLON",
    ";": "KC_SCOLON",
    "=": "KC_EQUAL",
    "?": "KC_QUES",
    "@": "KC_AT",
    "[": "KC_LBRC",
    "\\": "KC_BSLASH",
    "]": "KC_RBRC",
    "^": "KC_CIRC",
    "_": "KC_UNDS",
    "`": "KC_GRAVE",
    "`": "KC_GRAVE",
    "alt": "KC_LALT",
    "backspc": BACKSPACE,
    "bck": BACKSPACE,
    "bks": BACKSPACE,
    "btldr": "RESET",  # bootloader
    "chg_lay": "MAGIC_KEY",
    "ctrl": "KC_LCTRL",
    "del": "KC_DEL",
    "end": "KC_END",
    "ent": ENTER,
    "enter": ENTER,
    "esc": ESCAPE,
    "hld_cpgrm": "MO(CPRGMR)",
    "hld_kpd": "MO(KEYPAD)",
    "hld_med": "MO(MEDIA)",
    "hld_pgrm": "MO(PRGMR)",
    "home": "KC_HOME",
    "hyper": ESCAPE,
    "kb kb-arrows-down": "KC_DOWN",
    "kb kb-arrows-left": "KC_LEFT",
    "kb kb-arrows-right": "KC_RIGHT",
    "kb kb-arrows-up": "KC_UP",
    "kb kb-logo-linux-tux-ibm-invert": "KC_APP",
    "kb kb-multimedia-fastforward-end": "KC_MNXT",  # MEDIA_NEXT_TRACK
    "kb kb-multimedia-mute-1": "KC_MUTE",
    "kb kb-multimedia-pause": "KC_MPLY",  # MEDIA_PLAY_PAUSE
    "kb kb-multimedia-rewind-start": "KC_MPRV",  # MEDIA_PREV_TRACK
    "kb kb-multimedia-volume-down-1": VOLUME_DOWN,
    "kb kb-multimedia-volume-down-2": VOLUME_DOWN,
    "kb kb-multimedia-volume-up-1": VOLUME_UP,
    "kb kb-multimedia-volume-up-2": VOLUME_UP,
    "kb kb-unicode-screen-bright": "KC_BRIU",  # BRIGHTNESS_UP
    "kb kb-unicode-screen-dim": "KC_BRID",  # BRIGHTNESS_DOWN
    "l-shift": SHIFT,
    "lock": "LCA(KC_L)",
    "pgdn": "KC_PGDOWN",
    "pgup": "KC_PGUP",
    "r-shift": "KC_RSHIFT",
    "rpl mcr": "DM_PLY1",  # play the macro
    "shift": SHIFT,
    "space": SPACE,
    "spc": SPACE,
    "stp mcr": "DM_RSTP",  # stop recording a macro
    "str mcr": "DM_REC1",  # start recording a macro
    "super": "KC_LGUI",
    "tab": "KC_TAB",
    "{": "KC_LCBR",
    "|": "KC_PIPE",
    "}": "KC_RCBR",
    "~": "KC_TILD",
    '"': "KC_DQT",
    ("!", "1"): "KC_1",
    ("#", "3"): "KC_3",
    ("$", "4"): "KC_4",
    ("%", "5"): "KC_5",
    ("&", "7"): "KC_7",
    ("(", "9"): "KC_9",
    (")", "0"): "KC_0",
    ("*", "8"): "KC_8",
    ("+", "="): "KC_EQUAL",
    (":", ";"): "KC_SCOLON",
    ("<", ","): "KC_COMMA",
    (">", "."): "KC_DOT",
    ("?", "/"): "KC_SLASH",
    ("@", "2"): "KC_2",
    ("^", "6"): "KC_6",
    ("_", "-"): "KC_MINUS",
    ("ld bri", "dec", "inc"): "RGB_VAI",
    ("ld bri", "inc", "dec"): "RGB_VAD",
    ("ld hue", "dec", "inc"): "RGB_HUI",
    ("ld hue", "inc", "dec"): "RGB_HUD",
    ("ld mod", "bck", "fwd"): "RGB_MOD",  # RGB_MODE_FORWARD
    ("ld mod", "fwd", "bck"): "RGB_RMOD",  # RGB_MODE_REVERSE
    ("ld sat", "dec", "inc"): "RGB_SAI",
    ("ld sat", "inc", "dec"): "RGB_SAD",
    ("led", "", "toggle"): "RGB_TOG",
    ("{", "["): "KC_LBRC",
    ("|", "\\"): "KC_BSLASH",
    ("}", "]"): "KC_RBRC",
    ("~", "`"): "KC_GRAVE",
    ('"', "'"): "KC_QUOTE",
}
# Adding the common ASCII letters.
dict_keycode_mapper.update({char.lower(): f"KC_{char}" for char in ascii_uppercase})
# Adding the F keys (F1, F2, etc.)
dict_keycode_mapper.update({f"f{n}": f"KC_F{n}" for n in range(1, 13)})
# Adding some unicode characters
dict_keycode_mapper.update({char: f"UC({_get_unicode(char)})" for char in "àéèêçù£"})

C_CODE_SPACING = max(*[len(keycode) for keycode in dict_keycode_mapper.values()]) + 1
