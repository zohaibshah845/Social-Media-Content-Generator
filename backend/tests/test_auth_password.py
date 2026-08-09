import unittest

from app.auth import trim_password, get_password_hash


class AuthPasswordTests(unittest.TestCase):
    def test_trim_password_limits_utf8_bytes_for_bcrypt(self):
        password = "😀" * 20
        trimmed = trim_password(password)

        self.assertLessEqual(len(trimmed.encode("utf-8")), 72)
        self.assertIsInstance(get_password_hash(trimmed), str)


if __name__ == "__main__":
    unittest.main()
