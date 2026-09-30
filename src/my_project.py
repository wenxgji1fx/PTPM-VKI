import hashlib
import hmac
import logging
import os
import re
from typing import Final


BLACKLIST: Final[set[str]] = {
    "admin",
    "administrator",
    "root",
    "support",
    "test",
    "user",
    "qwerty",
    "system",
}

PHONE_RE: Final[re.Pattern[str]] = re.compile(
    r"^\+\d-\d{3}-\d{3}-\d{4}$"
)

EMAIL_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

USERNAME_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9_]+$"
)

CYRILLIC_RE: Final[re.Pattern[str]] = re.compile(
    r"^[А-Яа-яЁё0-9!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~\\]+$"
)

CYRILLIC_LOWER_RE: Final[re.Pattern[str]] = re.compile(r"[а-яё]")
CYRILLIC_UPPER_RE: Final[re.Pattern[str]] = re.compile(r"[А-ЯЁ]")
DIGIT_RE: Final[re.Pattern[str]] = re.compile(r"\d")
SPECIAL_RE: Final[re.Pattern[str]] = re.compile(
    r"[!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~\\]"
)
LATIN_RE: Final[re.Pattern[str]] = re.compile(r"[A-Za-z]")


def mask_password(password: str) -> str:
    """Возвращает безопасную детерминированную маску пароля."""
    key = os.getenv(
        "LAB_LOG_MASK_KEY",
        "ptpm-lab-1-local-mask-key",
    ).encode("utf-8")

    digest = hmac.new(
        key,
        password.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return f"<masked:{digest[:16]}>"


def _log_failure(
    logger: logging.Logger | None,
    login: str,
    password: str,
    password_confirmation: str,
    message: str,
) -> tuple[bool, str]:
    if logger is not None:
        logger.warning(
            "Неуспешный запрос | login=%r | password=%s | "
            "password_confirmation=%s | result=False | error=%s",
            login,
            mask_password(password),
            mask_password(password_confirmation),
            message,
        )
    return False, message


def _validate_login(login: str) -> str:
    if login == "":
        return "Логин не может быть пустым."

    normalized_login = login.lower()

    if normalized_login in BLACKLIST:
        return "Указанный логин находится в черном списке."

    if login.startswith("+"):
        if not PHONE_RE.fullmatch(login):
            return "Телефон должен соответствовать формату +x-xxx-xxx-xxxx."
        return ""

    if "@" in login:
        if not EMAIL_RE.fullmatch(login):
            return "Некорректный формат электронной почты."
        return ""

    if len(login) < 5:
        return "Строковый логин должен содержать не менее 5 символов."

    if not USERNAME_RE.fullmatch(login):
        return (
            "Строковый логин может содержать только латинские буквы, "
            "цифры и знак подчеркивания."
        )

    return ""


def _validate_password(password: str) -> str:
    if password == "":
        return "Пароль не может быть пустым."

    if len(password) < 7:
        return "Пароль должен содержать не менее 7 символов."

    if LATIN_RE.search(password):
        return "Пароль не должен содержать латинские буквы."

    if not CYRILLIC_RE.fullmatch(password):
        return (
            "Пароль может содержать только кириллицу, цифры "
            "и специальные символы без пробелов."
        )

    if not CYRILLIC_LOWER_RE.search(password):
        return "Пароль должен содержать хотя бы одну строчную букву."

    if not CYRILLIC_UPPER_RE.search(password):
        return "Пароль должен содержать хотя бы одну заглавную букву."

    if not DIGIT_RE.search(password):
        return "Пароль должен содержать хотя бы одну цифру."

    if not SPECIAL_RE.search(password):
        return "Пароль должен содержать хотя бы один специальный символ."

    return ""


def validate_registration(
    login: str,
    password: str,
    password_confirmation: str,
    logger: logging.Logger | None = None,
) -> tuple[bool, str]:
    """Проверяет регистрационные данные пользователя."""
    try:
        if logger is not None:
            logger.debug(
                "Получен запрос | login=%r | password=%s | "
                "password_confirmation=%s",
                login,
                mask_password(password),
                mask_password(password_confirmation),
            )

        login_error = _validate_login(login)
        if login_error:
            return _log_failure(
                logger, login, password, password_confirmation, login_error
            )

        password_error = _validate_password(password)
        if password_error:
            return _log_failure(
                logger, login, password, password_confirmation, password_error
            )

        if password != password_confirmation:
            return _log_failure(
                logger,
                login,
                password,
                password_confirmation,
                "Пароль и подтверждение пароля не совпадают.",
            )

        if logger is not None:
            logger.info(
                "Успешный запрос | login=%r | password=%s | "
                "password_confirmation=%s | result=True",
                login,
                mask_password(password),
                mask_password(password_confirmation),
            )

        return True, ""

    except Exception:
        if logger is not None:
            logger.exception(
                "Сбой валидации | login=%r | password=%s | "
                "password_confirmation=%s",
                login,
                mask_password(password),
                mask_password(password_confirmation),
            )
        return False, "Внутренняя ошибка при проверке данных."
