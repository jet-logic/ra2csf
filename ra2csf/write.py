from typing import IO
from struct import pack


def write_str(fh: IO[bytes], s=""):
    fh.write(pack("<I", len(s)))
    fh.write(s.encode("latin1"))


def write_wstr(fh: IO[bytes], s=""):
    e = s.encode("UTF-16-LE")
    fh.write(pack("<I", len(e) // 2))
    fh.write(bytes([(0xFF - b) for b in e]))


def write_entry(fh: IO[bytes], key, value="", flag=1, extra=None):
    fh.write(b" LBL")
    fh.write(pack("<I", flag))
    write_str(fh, key)
    fh.write(b"WRTS" if extra else b" RTS")
    write_wstr(fh, value)
    if extra:
        write_str(fh, extra)


def write(
    fh: IO[bytes], head=list[int], strings=list[tuple[str, str, int, str | None]]
):
    fh.write(pack("<IIIIII", *head))
    for v in strings:
        write_entry(fh, *v)
