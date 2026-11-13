import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, "main.py", *args],
                          cwd=ROOT, capture_output=True, text=True, check=False)


class CliTests(unittest.TestCase):
    def test_example(self):
        result = run(*["before.json","after.json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(set(data['changed'][0]['fields']), {'predecessor_dn','migration_state'})

    def test_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.json"
            source.write_text("[{\"object_guid\":\"invalid\",\"dn\":\"CN=Demo\",\"predecessor_dn\":null,\"migration_state\":0}]", encoding="utf-8")
            result = run(source, *["after.json"])
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
