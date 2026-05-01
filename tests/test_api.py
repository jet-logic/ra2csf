#!/usr/bin/python3

import json
from pathlib import Path
from struct import unpack
from tempfile import NamedTemporaryFile, TemporaryFile, gettempdir
from unittest import TestCase, main
from os import stat
from ra2csf.read import parse_file
from ra2csf.write import write
import ra2csf


file = "tests/ra2.csf"


class Test(TestCase):
    def test_read_write(self):
        head, strings = parse_file(file)
        (id,) = unpack("<I", b" FSC")
        print(" FSC", hex(id))
        self.assertEqual(id, head[0])
        self.assertEqual(3, head[1])
        self.assertGreater(head[2], 4000)
        self.assertGreater(head[3], 4000)
        self.assertEqual(0, head[4])
        self.assertEqual(0, head[5])
        # write
        with TemporaryFile() as wh:
            write(wh, strings)
            self.assertEqual(wh.tell(), stat(file).st_size)
            wh.seek(0)
            with open(file, "rb") as rh:
                self.assertEqual(wh.read(), rh.read())

    def test_load_dump(self):
        smap = ra2csf.load(file)
        with TemporaryFile() as wh:
            ra2csf.dump(smap, wh)
            self.assertEqual(wh.tell(), stat(file).st_size)
            wh.seek(0)
            with open(file, "rb") as rh:
                self.assertEqual(wh.read(), rh.read())

    def test_update(self):
        map1 = ra2csf.load(file)
        key = "GUI:SurpriseMe"
        orig = map1[key]
        val = "Boo!"
        map1[key] = val
        with NamedTemporaryFile(delete_on_close=False) as w1:
            w1.close()
            ra2csf.dump(map1, w1.name)
            # check
            with open(file, "rb") as rh, open(w1.name, "rb") as r1:
                self.assertNotEqual(r1.read(), rh.read())
                r1.seek(0)
                map2 = ra2csf.load(r1)
                self.assertEqual(map2[key], val)
            # reset
            map3 = {}
            map3[key] = orig
            ra2csf.update(w1.name, map3)
            with open(file, "rb") as rh, open(w1.name, "rb") as r1:
                self.assertEqual(r1.read(), rh.read())
                r1.seek(0)
                map2 = ra2csf.load(r1)
                self.assertEqual(map2[key], orig)

    def test_debug_csf(self):
        tmp = Path(gettempdir())
        csf_file = Path(file)
        if 1:
            csf_debug_file = tmp / f"{csf_file.stem}-debug{csf_file.suffix}"
            with csf_file.open("rb") as r1:
                smap = ra2csf.load(r1)
            for k, v in tuple(smap.items()):
                if isinstance(v, str):
                    smap[k] = k
                else:
                    smap[k] = (k, v[1])
            with csf_debug_file.open("bw") as w1:
                ra2csf.dump(smap, w1)
        if 1:
            csf_json_file = tmp / f"{csf_file.stem}.json"
            with csf_file.open("rb") as r1:
                smap = ra2csf.load(r1)
            with csf_json_file.open("w") as w1:
                json.dump(smap, w1, indent=True)


if __name__ == "__main__":
    main()
