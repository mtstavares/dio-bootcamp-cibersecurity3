"""Regressão da exploração local e preservação do login legítimo."""

import unittest

import app
from examples import app_vulneravel


class LoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixed = app.create_lab_database()
        cls.vulnerable = app_vulneravel.create_lab_database()

    @classmethod
    def tearDownClass(cls):
        cls.fixed.close()
        cls.vulnerable.close()

    def test_valid_login_in_both_versions(self):
        for module, db in ((app, self.fixed), (app_vulneravel, self.vulnerable)):
            with self.subTest(version=module.__name__):
                self.assertTrue(module.login(db, "aluna", "senha-laboratorio"))

    def test_wrong_password_in_both_versions(self):
        for module, db in ((app, self.fixed), (app_vulneravel, self.vulnerable)):
            with self.subTest(version=module.__name__):
                self.assertFalse(module.login(db, "aluna", "incorreta"))

    def test_reproduce_and_block_username_bypass(self):
        payload = "' OR 1=1 -- "
        self.assertTrue(app_vulneravel.login(self.vulnerable, payload, "incorreta"))
        self.assertFalse(app.login(self.fixed, payload, "incorreta"))

    def test_reproduce_and_block_password_bypass(self):
        payload = "' OR 1=1 -- "
        self.assertTrue(app_vulneravel.login(self.vulnerable, "aluna", payload))
        self.assertFalse(app.login(self.fixed, "aluna", payload))

    def test_fixed_handles_quotes_as_data(self):
        self.assertFalse(app.login(self.fixed, "d'ávila", "senha-laboratorio"))

    def test_fixed_unknown_user(self):
        self.assertFalse(app.login(self.fixed, "desconhecida", "senha-laboratorio"))

    def test_fixed_does_not_store_plaintext_password(self):
        salt, stored_hash = self.fixed.execute(
            "SELECT salt, password_hash FROM users WHERE username = ?", ("aluna",)
        ).fetchone()
        self.assertEqual(len(salt), 16)
        self.assertEqual(len(stored_hash), 32)
        self.assertNotEqual(stored_hash, b"senha-laboratorio")


if __name__ == "__main__":
    unittest.main()
