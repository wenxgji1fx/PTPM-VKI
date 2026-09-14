from logger_config import configure_logging
from registration_validator import validate_registration


def main() -> None:
    """Точка входа в программу."""
    logger = configure_logging()

    logger.info("Приложение запущено")

    try:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        password_confirmation = input("Повторите пароль: ")

        is_valid, message = validate_registration(
            login=login,
            password=password,
            password_confirmation=password_confirmation,
            logger=logger,
        )

        if is_valid:
            print("True")
            print("")
        else:
            print("False")
            print(message)
    except Exception:
        logger.exception("Непредвиденная ошибка при выполнении программы")
        print("False")
        print("Произошла непредвиденная ошибка.")
    finally:
        logger.info("Приложение завершено")


if __name__ == "__main__":
    main()
