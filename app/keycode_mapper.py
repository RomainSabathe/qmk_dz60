import re
from binascii import hexlify
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
            return (
                f"LSFT({_keycode_mapper(key)})"
                if is_shift
                else _keycode_mapper(key)
            )
        key = parts[0] if is_shift else parts[1]
        keycode = _keycode_mapper(key)
        if keycode in ["KC_LEFT", "KC_RIGHT", "KC_UP", "KC_DOWN"] and is_shift:
            return f"LSFT({keycode})"
        return keycode

    return (
        f"LSFT({_keycode_mapper(key)})" if is_shift else _keycode_mapper(key)
    )


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
    char = char.encode()
    unicode = hexlify(char).decode().upper()
    return f"0x{unicode}"


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
    "chg_lay": "MAGIC_KEY",
    "hld_kpd": "MO(KEYPAD)",
    "hld_pgrm": "MO(PRGMR)",
    "hld_med": "MO(MEDIA)",
    "": TRANSPARENT,
    "esc": ESCAPE,
    "hyper": ESCAPE,
    "tab": "KC_TAB",
    "spc": SPACE,
    "space": SPACE,
    "backspc": BACKSPACE,
    "bck": BACKSPACE,
    "bks": BACKSPACE,
    "del": "KC_DEL",
    "ent": ENTER,
    "enter": ENTER,
    "l-shift": SHIFT,
    "shift": SHIFT,
    "r-shift": "KC_RSHIFT",
    "ctrl": "KC_LCTRL",
    "alt": "KC_LALT",
    ("!", "1"): "KC_1",
    ("@", "2"): "KC_2",
    ("#", "3"): "KC_3",
    ("$", "4"): "KC_4",
    ("%", "5"): "KC_5",
    ("^", "6"): "KC_6",
    ("&", "7"): "KC_7",
    ("*", "8"): "KC_8",
    ("(", "9"): "KC_9",
    (")", "0"): "KC_0",
    ("_", "-"): "KC_MINUS",
    ("+", "="): "KC_EQUAL",
    ("{", "["): "KC_LBRC",
    ("}", "]"): "KC_RBRC",
    (":", ";"): "KC_SCOLON",
    ('"', "'"): "KC_QUOTE",
    ("|", "\\"): "KC_BSLASH",
    ("<", ","): "KC_COMMA",
    (">", "."): "KC_DOT",
    ("?", "/"): "KC_SLASH",
    ("~", "`"): "KC_GRAVE",
    "=": "KC_EQUAL",
    "[": "KC_LBRC",
    "]": "KC_RBRC",
    ";": "KC_SCOLON",
    "'": "KC_QUOTE",
    "\\": "KC_BSLASH",
    ",": "KC_COMMA",
    ".": "KC_DOT",
    "/": "KC_SLASH",
    "`": "KC_GRAVE",
    "%": "KC_PERC",
    "~": "KC_TILD",
    "!": "KC_EXLM",
    "?": "KC_QUES",
    "@": "KC_AT",
    "#": "KC_HASH",
    "$": "KC_DLR",
    "^": "KC_CIRC",
    "&": "KC_AMPR",
    "*": "KC_ASTR",
    "+": "KC_PLUS",
    "_": "KC_UNDS",
    "(": "KC_LPRN",
    ")": "KC_RPRN",
    "{": "KC_LCBR",
    "}": "KC_RCBR",
    ":": "KC_COLON",
    '"': "KC_DQT",
    "|": "KC_PIPE",
    "`": "KC_GRAVE",
    "-": "KC_MINUS",
    "home": "KC_HOME",
    "pgdn": "KC_PGDOWN",
    "pgup": "KC_PGUP",
    "end": "KC_END",
    "lock": "LCA(KC_L)",
    "kb kb-arrows-left": "KC_LEFT",
    "kb kb-arrows-right": "KC_RIGHT",
    "kb kb-arrows-up": "KC_UP",
    "kb kb-arrows-down": "KC_DOWN",
    "kb kb-unicode-screen-dim": "KC_BRID",  # BRIGHTNESS_DOWN
    "kb kb-unicode-screen-bright": "KC_BRIU",  # BRIGHTNESS_UP
    "kb kb-multimedia-rewind-start": "KC_MPRV",  # MEDIA_PREV_TRACK
    "kb kb-multimedia-fastforward-end": "KC_MNXT",  # MEDIA_NEXT_TRACK
    "kb kb-multimedia-pause": "KC_MPLY",  # MEDIA_PLAY_PAUSE
    "kb kb-multimedia-volume-down-1": VOLUME_DOWN,
    "kb kb-multimedia-volume-down-2": VOLUME_DOWN,
    "kb kb-multimedia-volume-up-1": VOLUME_UP,
    "kb kb-multimedia-volume-up-2": VOLUME_UP,
    "kb kb-multimedia-mute-1": "KC_MUTE",
    "kb kb-logo-linux-tux-ibm-invert": "KC_APP",
    ("ld bri", "dec", "inc"): "RGB_VAI",
    ("ld bri", "inc", "dec"): "RGB_VAD",
    ("ld sat", "dec", "inc"): "RGB_SAI",
    ("ld sat", "inc", "dec"): "RGB_SAD",
    ("ld hue", "dec", "inc"): "RGB_HUI",
    ("ld hue", "inc", "dec"): "RGB_HUD",
    ("ld mod", "bck", "fwd"): "RGB_MOD",  # RGB_MODE_FORWARD
    ("ld mod", "fwd", "bck"): "RGB_RMOD",  # RGB_MODE_REVERSE
    ("led", "", "toggle"): "RGB_TOG",
    "str mcr": "DM_REC1",  # start recording a macro
    "stp mcr": "DM_RSTP",  # stop recording a macro
    "rpl mcr": "DM_PLY1",  # play the macro
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
    "btldr": "RESET"  # bootloader
}
# Adding the common ASCII letters.
dict_keycode_mapper.update(
    {char.lower(): f"KC_{char}" for char in ascii_uppercase}
)
# Adding the F keys (F1, F2, etc.)
dict_keycode_mapper.update({f"f{n}": f"KC_F{n}" for n in range(1, 13)})
# Adding some unicode characters
dict_keycode_mapper.update(
    {char: f"UC({_get_unicode(char)})" for char in "àéèêç"}
)

C_CODE_SPACING = (
    max(*[len(keycode) for keycode in dict_keycode_mapper.values()]) + 1
)
