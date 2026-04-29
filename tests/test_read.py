#!/usr/bin/python3
from struct import unpack
from tempfile import TemporaryFile
from unittest import TestCase, main
from os import stat
from ra2csf.read import parse_file
from ra2csf.write import write


class Test(TestCase):
    def test_read_write(self):
        file = "tests/ra2.csf"
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
            # print(wh.tell())
            self.assertEqual(wh.tell(), stat(file).st_size)
            wh.seek(0)
            with open(file, "rb") as rh:
                self.assertEqual(wh.read(), rh.read())


if __name__ == "__main__":
    main()
