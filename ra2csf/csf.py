from .read import parse_file, parse
from .write import write


def load(file=""):
    head, strings = parse_file(file)
    return dict((v[0], v[1]) for v in strings)


def dump(file="", strmap: dict[str, str] = {}, **kwargs):
    with open(file, "wb") as wh:
        write(wh, strmap, **kwargs)


def update(file="", strmap: dict[str, str] = {}, **kwargs):
    if isinstance(file, str):
        head, strings = parse_file(file)
    else:
        head, strings = parse(file)
    smap = dict((v[0], v[1:]) for v in strings)
    for k, v in strmap.items():
        smap[k] = v
    with open(file, "wb") as wh:
        write(wh, smap, head, **kwargs)
