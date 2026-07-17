import hashlib

import TimePulse


def test_password_hash_is_salted_and_verifiable():
    first = TimePulse.hash_password("correct horse")
    second = TimePulse.hash_password("correct horse")

    assert first != second
    assert TimePulse.verify_password("correct horse", first)
    assert not TimePulse.verify_password("wrong password", first)


def test_legacy_sha256_password_is_supported():
    legacy = hashlib.sha256(b"legacy-password").hexdigest()
    assert TimePulse.verify_password("legacy-password", legacy)
    assert not TimePulse.verify_password("incorrect", legacy)


def test_new_password_validation():
    assert TimePulse.validate_new_password("")
    assert TimePulse.validate_new_password("     ")
    assert TimePulse.validate_new_password("12345")
    assert TimePulse.validate_new_password("123456") is None
