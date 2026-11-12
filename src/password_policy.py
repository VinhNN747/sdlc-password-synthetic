MIN_PASSWORD_LENGTH = 12
PASSWORD_LENGTH_ERROR = "Password must be at least 12 characters"


def validate_password(password: object) -> None:
    if not isinstance(password, str) or len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(PASSWORD_LENGTH_ERROR)