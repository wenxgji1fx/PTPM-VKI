import unittest

from src.my_project import mask_password, validate_registration


VALID_PASSWORD = "Пароль1!"


class TestRegistrationValidation(unittest.TestCase):
    def test_accepts_valid_string_login(self):
        self.assertEqual(validate_registration("student_1", VALID_PASSWORD, VALID_PASSWORD), (True, ""))

    def test_accepts_valid_phone_login(self):
        self.assertEqual(validate_registration("+7-999-123-4567", VALID_PASSWORD, VALID_PASSWORD), (True, ""))

    def test_accepts_valid_email_login(self):
        self.assertEqual(validate_registration("student@example.com", VALID_PASSWORD, VALID_PASSWORD), (True, ""))

    def test_rejects_empty_login(self):
        result, message = validate_registration("", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("пустым", message)

    def test_rejects_blacklisted_login(self):
        result, message = validate_registration("admin", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("черном списке", message)

    def test_rejects_invalid_phone_format(self):
        result, message = validate_registration("+7 999 123 4567", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("+x-xxx-xxx-xxxx", message)

    def test_rejects_invalid_email_format(self):
        result, message = validate_registration("student@", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("электронной почты", message)

    def test_rejects_short_string_login(self):
        result, message = validate_registration("abc", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("не менее 5", message)

    def test_rejects_cyrillic_in_string_login(self):
        result, message = validate_registration("студент", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("латинские буквы", message)

    def test_rejects_empty_password(self):
        result, message = validate_registration("student", "", "")
        self.assertFalse(result)
        self.assertIn("пустым", message)

    def test_rejects_short_password(self):
        result, message = validate_registration("student", "Аб1!", "Аб1!")
        self.assertFalse(result)
        self.assertIn("не менее 7", message)

    def test_rejects_latin_letters_in_password(self):
        result, message = validate_registration("student", "Password1!", "Password1!")
        self.assertFalse(result)
        self.assertIn("латинские", message)

    def test_requires_lowercase_letter(self):
        result, message = validate_registration("student", "ПАРОЛЬ1!", "ПАРОЛЬ1!")
        self.assertFalse(result)
        self.assertIn("строчную", message)

    def test_requires_uppercase_letter(self):
        result, message = validate_registration("student", "пароль1!", "пароль1!")
        self.assertFalse(result)
        self.assertIn("заглавную", message)

    def test_requires_digit(self):
        result, message = validate_registration("student", "Пароль!!", "Пароль!!")
        self.assertFalse(result)
        self.assertIn("цифру", message)

    def test_requires_special_character(self):
        result, message = validate_registration("student", "Пароль12", "Пароль12")
        self.assertFalse(result)
        self.assertIn("специальный", message)

    def test_rejects_space_in_password(self):
        result, message = validate_registration("student", "Пароль 1!", "Пароль 1!")
        self.assertFalse(result)
        self.assertIn("без пробелов", message)

    def test_rejects_password_confirmation_mismatch(self):
        result, message = validate_registration("student", "Пароль1!", "Другой2!")
        self.assertFalse(result)
        self.assertIn("не совпадают", message)

    def test_same_password_has_same_mask(self):
        self.assertEqual(mask_password("Пароль1!"), mask_password("Пароль1!"))

    def test_different_passwords_have_different_masks(self):
        self.assertNotEqual(mask_password("Пароль1!"), mask_password("Пароль2!"))


if __name__ == "__main__":
    unittest.main()
