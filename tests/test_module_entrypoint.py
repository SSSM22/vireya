import subprocess
import sys
import unittest
from pathlib import Path


class ModuleEntrypointTests(unittest.TestCase):
    def test_python_can_import_vireya_api_from_repo_root(self):
        repo_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-c", "import vireya.api"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)


if __name__ == "__main__":
    unittest.main()
