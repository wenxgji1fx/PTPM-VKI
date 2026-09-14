import unittest

from registration_validator import mask_password, validate_registration


VALID_PASSWORD = "Пароль1!"


class RegistrationValidatorTests(unittest.TestCase):
    def test_valid_string_login(self) -> None:
        self.assertEqual(
            validate_registration("student_1", VALID_PASSWORD, VALID_PASSWORD),
            (True, ""),
        )

    def test_valid_phone_login(self) -> None:
        self.assertEqual(
            validate_registration("+7-999-123-4567", VALID_PASSWORD, VALID_PASSWORD),
            (True, ""),
        )

    def test_valid_email_login(self) -> None:
        self.assertEqual(
            validate_registration(
                "student@example.com",
                VALID_PASSWORD,
                VALID_PASSWORD,
            ),
            (True, ""),
        )

    def test_empty_login(self) -> None:
        result, message = validate_registration("", VALID_PASSWORD, VALID_PASSWORD)
        self.assertFalse(result)
        self.assertIn("пустым", message)

    def test_blacklisted_login(self) -> None:
        result, message = validate_registration(
            "admin",
            VALID_PASSWORD,
            VALID_PASSWORD,
        )
        self.assertFalse(result)
        self.assertIn("черном списке", message)

    def test_invalid_phone(self) -> None:
        result, message = validate_registration(
            "+7 999 123 4567",
            VALID_PASSWORD,
            VALID_PASSWORD,
        )
        self.assertFalse(result)
        self.assertIn("+x-xxx-xxx-xxxx", message)

    def test_invalid_email(self) -> None:
        result, message = validate_registration(
            "student@",
            VALID_PASSWORD,
            VALID_PASSWORD,
        )
        self.assertFalse(result)
        self.assertIn("электронной почты", message)

    def test_short_username(self) -> None:
        result, message = validate_registration(
            "abc",
            VALID_PASSWORD,
            VALID_PASSWORD,
        )
        self.assertFalse(result)
        self.assertIn("не менее 5", message)

    def test_invalid_username_characters(self) -> None:
        result, message = validate_registration(
            "студент",
            VALID_PASSWORD,
            VALID_PASSWORD,
        )
        self.assertFalse(result)
        self.assertIn("латинские буквы", message)

    def test_empty_password(self) -> None:
        result, message = validate_registration("student", "", "")
        self.assertFalse(result)
        self.assertIn("пустым", message)

    def test_short_password(self) -> None:
        result, message = validate_registration("student", "Аб1!", "Аб1!")
        self.assertFalse(result)
        self.assertIn("не менее 7", message)

    def test_latin_letters_are_forbidden(self) -> None:
        result, message = validate_registration(
            "student",
            "Password1!",
            "Password1!",
        )
        self.assertFalse(result)
        self.assertIn("латинские", message)

    def test_password_requires_lowercase(self) -> None:
        result, message = validate_registration(
            "student",
            "ПАРОЛЬ1!",
            "ПАРОЛЬ1!",
        )
        self.assertFalse(result)
        self.assertIn("строчную", message)

    def test_password_requires_uppercase(self) -> None:
        result, message = validate_registration(
            "student",
            "пароль1!",
            "пароль1!",
        )
        self.assertFalse(result)
        self.assertIn("заглавную", message)

    def test_password_requires_digit(self) -> None:
        result, message = validate_registration(
            "student",
            "Пароль!!",
            "Пароль!!",
        )
        self.assertFalse(result)
        self.assertIn("цифру", message)

    def test_password_requires_special_character(self) -> None:
        result, message = validate_registration(
            "student",
            "Пароль12",
            "Пароль12",
        )
        self.assertFalse(result)
        self.assertIn("специальный", message)

    def test_password_rejects_space(self) -> None:
        result, message = validate_registration(
            "student",
            "Пароль 1!",
            "Пароль 1!",
        )
        self.assertFalse(result)
        self.assertIn("без пробелов", message)

    def test_password_confirmation_must_match(self) -> None:
        result, message = validate_registration(
            "student",
            "Пароль1!",
            "Другой2!",
        )
        self.assertFalse(result)
        self.assertIn("не совпадают", message)

    def test_mask_is_deterministic(self) -> None:
        self.assertEqual(mask_password("Пароль1!"), mask_password("Пароль1!"))

    def test_different_passwords_have_different_masks(self) -> None:
        self.assertNotEqual(mask_password("Пароль1!"), mask_password("Пароль2!"))

    def test_mask_does_not_contain_original_password(self) -> None:
        password = "Пароль1!"
        self.assertNotIn(password, mask_password(password))


if __name__ == "__main__":
    unittest.main()
