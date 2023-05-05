from src.auth.password import get_password_hash, verify_password
from src.auth.services import create_access_token, decode_token_data


def test_jwt_full_work():
    """
    Тест роботи методів, які використовують JWT.
    Шифрує інформацію про користувача у JWT, потім його розшифровує.
    Потім відбувається перевірка еквівалентності отриманого email з введеним
    """
    email = "test@test.com"
    token = create_access_token({"sub": email})
    assert decode_token_data(token).email == email


def test_decode_jwt_with_incorrect_data():
    assert decode_token_data("incorrect") is None


def test_hash_and_verify_password():
    password = "test1234test"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)


def test_verify_password_with_incorrect_data():
    hashed_password = get_password_hash("test1234test")
    assert not verify_password("incorrect", hashed_password)
