__version__ = "0.0.3"

from .read import parse_file, parse
from .write import write


def load(file="", head=None):
    if isinstance(file, str):
        _head, strings = parse_file(file)
    else:
        _head, strings = parse(file)
    if head is not None:
        assert isinstance(head, list)
        head.clear()
        head.extend(_head)
    return dict((v[0], [v[1], v[2]] if v[2] else v[1]) for v in strings)


def dump(strmap: dict[str, str] = {}, file="", **kwargs):
    if isinstance(file, str):
        with open(file, "wb") as wh:
            dump(strmap, wh, **kwargs)
    else:
        write(file, strmap, **kwargs)


def update(file="", strmap: dict[str, str] = {}, **kwargs):
    head = []
    smap = load(file, head)
    for k, v in strmap.items():
        smap[k] = v
    with open(file, "wb") as wh:
        write(wh, smap, head, **kwargs)
