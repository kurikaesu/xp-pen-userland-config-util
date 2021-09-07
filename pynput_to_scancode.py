def get_keymap():
    keymap = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 11,
        '-': 12,
        '=': 13,
        'key.backspace': 14,
        'key.tab': 15,
        'q': 16,
        'w': 17,
        'e': 18,
        'r': 19,
        't': 20,
        'y': 21,
        'u': 22,
        'i': 23,
        'o': 24,
        'p': 25,
        '[': 26,
        ']': 27,
        'key.enter': 28,
        'key.ctrl': 29,
        'a': 30,
        's': 31,
        'd': 32,
        'f': 33,
        'g': 34,
        'h': 35,
        'j': 36,
        'k': 37,
        'l': 38,
        ';': 39,
        'key.shift': 42,
        '\\\\': 43,
        'z': 44,
        'x': 45,
        'c': 46,
        'v': 47,
        'b': 48,
        'n': 49,
        'm': 50,
        ',': 51,
        '.': 52,
        '/': 53,
        'key.shift_r': 54,
        'key.alt': 56,
        'key.space': 57,
        '<65328>': 58,
        'key.delete': 111
    }

    return keymap


def get_reversed_keymap():
    keymap = {v: k for k, v in get_keymap().items()}
    return keymap


def to_scancode(key):
    keymap = get_keymap()

    lower_key = key.lower()

    if lower_key in keymap:
        return keymap[lower_key]

    return key


def from_scancode(code):
    keymap = get_reversed_keymap()

    if code in keymap:
        return keymap[code]

    return code
