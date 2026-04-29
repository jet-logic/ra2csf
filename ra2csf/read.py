from typing import IO
from struct import unpack


def read_str(fh: IO[bytes]):
    (n,) = unpack("<I", fh.read(4))
    return fh.read(n).decode("latin1")


def read_wstr(fh: IO[bytes]):
    (n,) = unpack("<I", fh.read(4))
    return bytes([0xFF - b for b in fh.read(n * 2)]).decode("UTF-16-LE")


def read_int(fh: IO[bytes]) -> int:
    (n,) = unpack("<I", fh.read(4))
    return n


def read_entry(fh: IO[bytes], sig=b""):
    if not sig:
        sig = fh.read(4)
    assert sig == b" LBL", f"sig = {sig}"
    flag = read_int(fh)
    key = read_str(fh)
    kind = fh.read(4)
    value = read_wstr(fh)
    if kind == b"WRTS":
        extra = read_str(fh)
        assert extra
        # print("Extra", (key, value, extra))
    else:
        assert kind == b" RTS"
        extra = None

    return key, value, flag, extra


def read_entries(fh: IO[bytes]):
    b = fh.read(4)
    while b == b" LBL":
        key, value, flag, extra = read_entry(fh, b)
        yield key, value, extra, flag
        b = fh.read(4)


def parse(fh: IO[bytes]):
    # identifier, version, labels, extra_value, flag, language
    head: tuple[int] = unpack("<IIIIII", fh.read(6 * 4))
    strings = tuple(read_entries(fh))
    return head, strings


def parse_file(csf_file=""):
    with open(csf_file, "br") as rh:
        return parse(rh)
