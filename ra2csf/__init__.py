__version__ = "0.0.2"

from .read import parse_file, parse
from .write import write


def load(file=""):
    if isinstance(file, str):
        head, strings = parse_file(file)
    else:
        head, strings = parse(file)
    return dict((v[0], (v[1], v[2]) if v[2] else v[1]) for v in strings)


def dump(strmap: dict[str, str] = {}, file="", **kwargs):
    if isinstance(file, str):
        with open(file, "wb") as wh:
            dump(strmap, wh, **kwargs)
    else:
        write(file, strmap, **kwargs)


def update(file="", strmap: dict[str, str] = {}, **kwargs):
    if isinstance(file, str):
        head, strings = parse_file(file)
    else:
        head, strings = parse(file)
    smap = dict((v[0], (v[1], v[2]) if v[2] else v[1]) for v in strings)
    for k, v in strmap.items():
        smap[k] = v
    with open(file, "wb") as wh:
        write(wh, smap, head, **kwargs)
