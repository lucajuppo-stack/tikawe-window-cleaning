import pathlib
import secrets

KEY_FILE = pathlib.Path(".secret_key")


def load_secret_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_text(encoding="utf-8").strip()
    key = secrets.token_hex(16)
    KEY_FILE.write_text(key, encoding="utf-8")
    return key


secret_key = load_secret_key()
