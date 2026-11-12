import pytest

from password_policy import PASSWORD_LENGTH_ERROR, validate_password


@pytest.mark.parametrize(
    "password",
    [
        "a" * 11,
        None,
        123,
    ],
)
def test_rejects_short_or_non_string_passwords(password: object) -> None:
    with pytest.raises(ValueError, match=f"^{PASSWORD_LENGTH_ERROR}$"):
        validate_password(password)


@pytest.mark.parametrize(
    "password",
    [
        "a" * 12,
        "a" * 13,
        " " * 12,
    ],
)
def test_accepts_passwords_with_at_least_twelve_characters(password: str) -> None:
    assert validate_password(password) is None