import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vireya.auth import AuthService
from vireya.storage import JsonStore


class ApiAndAuthTests(unittest.TestCase):
    def test_auth_service_registers_and_authenticates(self):
        service = AuthService()
        service.register("manager", "secret", "manager")
        user = service.authenticate("manager", "secret")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "manager")

    def test_json_store_persists_data(self):
        store = JsonStore(Path(__file__).resolve().parent / "tmp_store.json")
        store.append("orders", {"id": 1})
        self.assertEqual(store.get("orders")[-1]["id"], 1)


if __name__ == "__main__":
    unittest.main()
