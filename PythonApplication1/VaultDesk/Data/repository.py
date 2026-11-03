
import json
import os
import sqlite3
from pathlib import Path

from cryptography.fernet import InvalidToken

from VaultDesk.Services.security import make_cipher


DB_PATH = Path.home() / ".vaultdesk" / "vault.db"
CHECK_VALUE = b"VAULTDESK_UNLOCKED_V1"


class VaultRepository:
    def __init__(self, path=DB_PATH):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.db = sqlite3.connect(str(self.path))
        self.cipher = None

        self.db.execute(
            "CREATE TABLE IF NOT EXISTS settings "
            "(name TEXT PRIMARY KEY, value BLOB NOT NULL)"
        )

        self.db.execute(
            "CREATE TABLE IF NOT EXISTS entries "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "payload BLOB NOT NULL)"
        )

        self.db.commit()

    def _setting(self, name):
        row = self.db.execute(
            "SELECT value FROM settings WHERE name = ?",
            (name,)
        ).fetchone()

        return row[0] if row else None

    def is_initialized(self):
        return self._setting("salt") is not None

    def initialize(self, password):
        if self.is_initialized():
            raise ValueError(
                "Tresor ist bereits eingerichtet."
            )

        if len(password) < 12:
            raise ValueError(
                "Master-Passwort: mindestens 12 Zeichen."
            )

        salt = os.urandom(16)
        cipher = make_cipher(password, salt)

        with self.db:
            self.db.execute(
                "INSERT INTO settings (name, value) "
                "VALUES (?, ?)",
                ("salt", salt)
            )

            self.db.execute(
                "INSERT INTO settings (name, value) "
                "VALUES (?, ?)",
                (
                    "verifier",
                    cipher.encrypt(CHECK_VALUE)
                )
            )

        self.cipher = cipher

    def unlock(self, password):
        salt = self._setting("salt")
        verifier = self._setting("verifier")

        if salt is None or verifier is None:
            raise ValueError(
                "Tresor ist nicht eingerichtet "
                "oder beschädigt."
            )

        candidate = make_cipher(password, salt)

        try:
            if candidate.decrypt(verifier) != CHECK_VALUE:
                return False

        except InvalidToken:
            return False

        self.cipher = candidate
        return True

    def _check(self):
        if self.cipher is None:
            raise RuntimeError("Tresor ist gesperrt.")

    def list_entries(self):
        self._check()

        rows = self.db.execute(
            "SELECT id, payload FROM entries "
            "ORDER BY id DESC"
        ).fetchall()

        result = []

        for entry_id, payload in rows:
            entry = json.loads(
                self.cipher.decrypt(payload)
                .decode("utf-8")
            )

            entry["id"] = entry_id
            result.append(entry)

        return result

    def save_entry(self, entry, entry_id=None):
        self._check()

        data = {
            "title": entry["title"],
            "username": entry["username"],
            "password": entry["password"],
            "website": entry["website"],
        }

        payload = self.cipher.encrypt(
            json.dumps(data).encode("utf-8")
        )

        with self.db:
            if entry_id is None:
                self.db.execute(
                    "INSERT INTO entries (payload) "
                    "VALUES (?)",
                    (payload,)
                )
            else:
                self.db.execute(
                    "UPDATE entries SET payload = ? "
                    "WHERE id = ?",
                    (payload, entry_id)
                )

    def delete_entry(self, entry_id):
        self._check()

        with self.db:
            self.db.execute(
                "DELETE FROM entries WHERE id = ?",
                (entry_id,)
            )

    def close(self):
        self.cipher = None
        self.db.close()

