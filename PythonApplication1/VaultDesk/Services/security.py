
import base64
import secrets
import string

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


ITERATIONS = 600_000
SYMBOLS = "!@#$%&*?-_"


def make_cipher(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )

    key = kdf.derive(master_password.encode("utf-8"))
    return Fernet(base64.urlsafe_b64encode(key))


def generate_password(
    length=20,
    use_digits=True,
    use_symbols=True
):
    if length < 8:
        raise ValueError("Mindestens 8 Zeichen erforderlich.")

    groups = [
        string.ascii_lowercase,
        string.ascii_uppercase
    ]

    if use_digits:
        groups.append(string.digits)

    if use_symbols:
        groups.append(SYMBOLS)

    alphabet = "".join(groups)

    characters = [
        secrets.choice(group)
        for group in groups
    ]

    characters.extend(
        secrets.choice(alphabet)
        for _ in range(length - len(characters))
    )

    for i in range(len(characters) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        characters[i], characters[j] = (
            characters[j], characters[i]
        )

    return "".join(characters)

