#!/usr/bin/python3

import json
from unittest import TestCase, main
from subprocess import run

file = "tests/ra2.csf"


class Test(TestCase):
    def test_1(self):
        run(
            rf"""
         python -m ra2csf d -f yaml {file} /tmp/ra2.yaml
        """,
            shell=True,
            check=True,
        )
        import yaml

        with open(r"/tmp/ra2.yaml", "rb") as rh:
            d = yaml.safe_load(rh)

        self.assertEqual(d["THEME:MadRap"], "Hell March")
        self.assertEqual(d["MSG:LittleExperience"], "green")
        self.assertNotIn("ABC:123", d)
        self.assertIn("THEME:Scout", d)

    def test_2(self):
        csf2 = "/tmp/ra2.csf"
        with open(r"/tmp/add.json", "w") as rh:
            d = json.dump({"MSG:LittleExperience": "blue"}, rh)
        run(
            rf"""python -m ra2csf merge {csf2} {file} /tmp/add.json - << 'EOD'
THEME:MadRap: Lone Troop
EOD
        """,
            shell=True,
            check=True,
        )
        run(rf"""python -m ra2csf dump {csf2} /tmp/ra2.json""", shell=True, check=True)
        with open(r"/tmp/ra2.json", "rb") as rh:
            d = json.load(rh)
        self.assertEqual(d["THEME:MadRap"], "Lone Troop")
        self.assertEqual(d["MSG:LittleExperience"], "blue")
        run(
            rf"""python -m ra2csf update {csf2} - << 'EOD'
{{
    "THEME:MadRap":"Hell March",
    "MSG:LittleExperience":"green"
}}
EOD
        """,
            shell=True,
            check=True,
        )
        with open(file, "rb") as rh, open(csf2, "rb") as r1:
            self.assertEqual(r1.read(), rh.read())


if __name__ == "__main__":
    main()
