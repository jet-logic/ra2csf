from .write import write
from . import load


def as_sink(path="-", mode="wb"):
    if path and path != "-":
        return open(path, mode)
    from sys import stdout

    return stdout.buffer if "b" in mode else stdout


def as_source(path="-", mode="rb"):
    if path and path != "-":
        return open(path, mode)
    from sys import stdin

    return stdin.buffer if "b" in mode else stdin


def _merge(csf_file="", sources=(), update=False):
    if update:
        cs_map = load(csf_file)
    else:
        cs_map = {}

    for v in sources:
        with as_source(v, "rb") as rh:
            b = rh.peek(32)
            if b.startswith(b" FSC"):
                d = load(rh)
            else:
                b = b.strip()
                if b.startswith(b"{") or b.startswith(b"["):
                    import json

                    d = json.load(rh)
                else:
                    import yaml

                    d = yaml.safe_load(rh)
        assert isinstance(d, dict)
        cs_map.update(d)
    if cs_map:
        with as_sink(csf_file) as wh:
            write(wh, cs_map)


def _dump(csf_file="", format="", out_file=""):
    with as_source(csf_file) as rh:
        cs_map = load(rh)
    if format == "yaml":
        import yaml

        with as_sink(out_file, "w") as wh:
            yaml.dump(cs_map, wh, default_flow_style=False)
    else:
        import json

        with as_sink(out_file, "w") as wh:
            json.dump(cs_map, wh, indent=True)


def main():
    from argparse import ArgumentParser

    cli = ArgumentParser(
        prog="ra2csf",
        description="dump, merge, update Command & Conquer: Red Alert 2 / Command & Conquer: Yuri's Revenge CSF files",
    )
    cli.set_defaults(_what="")

    subparsers = cli.add_subparsers()
    # dump
    sub = subparsers.add_parser("dump", aliases=("d"), help="Dump .csf file as JSON")
    sub.add_argument("--format", "-f", help="dump format", choices=["json", "yaml"])
    sub.add_argument("csf_file", help="source .csf file")
    sub.add_argument("out_file", help="output file")
    sub.set_defaults(_what="d")
    # merge
    sub = subparsers.add_parser(
        "merge", aliases=("m",), help="merge to .csf file, json, yaml"
    )
    sub.add_argument("csf_file", help=".csf file to write to")
    sub.add_argument("sources", help="source files to merge", nargs="+")
    sub.set_defaults(_what="m")
    # update
    sub = subparsers.add_parser(
        "update", aliases=("u",), help="add entries to a .csf file"
    )
    sub.add_argument("csf_file", help=".csf file to update")
    sub.add_argument("sources", help="source files to merge", nargs="+")
    sub.set_defaults(_what="u")
    # parse
    ns = cli.parse_args().__dict__
    what = ns.pop("_what") or ""
    if what.startswith("d"):
        _dump(**ns)
    else:
        _merge(**ns, update=what.startswith("u"))


if __name__ == "__main__":
    main()
