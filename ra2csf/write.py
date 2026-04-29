from typing import IO
from struct import pack


def write_str(fh: IO[bytes], s=""):
    fh.write(pack("<I", len(s)))
    fh.write(s.encode("latin1"))


def write_wstr(fh: IO[bytes], s=""):
    e = s.encode("UTF-16-LE")
    fh.write(pack("<I", len(e) // 2))
    fh.write(bytes([(0xFF - b) for b in e]))


def write_entry(fh: IO[bytes], key, value="", extra=None, flag=1):
    # if extra:
    #     print(key, value, extra)
    fh.write(b" LBL")
    fh.write(pack("<I", flag))
    write_str(fh, key)
    fh.write(b"WRTS" if extra else b" RTS")
    write_wstr(fh, value)
    if extra:
        assert isinstance(extra, str)
        assert extra
        write_str(fh, extra)


def write(
    fh: IO[bytes],
    strings=list[tuple[str, str, str | None, int]],
    head: list[int] = [],
    version=3,
    flags=0,
    language=0,
    identifier=0x43534620,  # ' FSC'
):
    n = len(strings)
    if not head:
        head = (identifier, version, n, n, flags, language)
    fh.write(pack("<IIIIII", *head))

    if isinstance(strings, dict):
        for key, v in strings.items():
            assert isinstance(key, str)
            if isinstance(v, (tuple, list)):
                assert v[0]
                # print(v)
                write_entry(fh, key, *v)
            else:
                assert isinstance(v, str)
                # assert v
                write_entry(fh, key, v)
    else:
        for v in strings:
            write_entry(fh, *v)
