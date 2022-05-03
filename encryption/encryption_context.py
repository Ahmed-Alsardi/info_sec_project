import logging
import os

import bcrypt
from Crypto.Hash import SHA3_256

from encryption.encryption_utils import EncryptionUtils as utils

logging.basicConfig(level=logging.INFO)


class EncryptionContext:
    def __init__(
            self,
            is_new_user: bool,
            user_passphrase: str,
            username: str,
        user_public_key: str = None,
    ):
        sha3_256 = SHA3_256.new()
        self.__user_passphrase = sha3_256.update(
            user_passphrase.encode("utf-8")
        ).hexdigest()
        self.__username = username
        self.__public_key = user_public_key
        if is_new_user:
            self._init_user_context()
        else:
            self._load_user_context()

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(password, hashed_password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @property
    def public_key(self) -> bytes:
        return self.__public_key

    @property
    def username(self) -> str:
        return self.__username

    def _init_user_context(self):
        rsa_public_key, private_key = utils.generate_public_private_keys(
            self.__user_passphrase
        )
        self.__public_key = rsa_public_key
        self.__private_key = private_key
        path = os.path.dirname(__file__)
        with open(f"{path}/keys/{self.username}_pk.pem", "wb") as f:
            f.write(private_key)
        logging.info(f"created new user context for {self.username}")

    def _load_user_context(self):
        assert self.public_key is not None
        path = os.path.dirname(__file__)
        self.__private_key = open(f"{path}/keys/{self.username}_pk.pem", "rb").read()
        logging.info(f"loaded user context for {self.username}")

    @staticmethod
    def encrypt_message(
            message: bytes, receiver_public_key: bytes
    ) -> tuple[bytes, bytes]:
        session_key = utils.generate_session_key()
        cipher_text = utils.encrypt_message_with_session_key(message, session_key)
        enc_session_key = utils.encrypt_session_key_with_public_key(
            session_key, receiver_public_key
        )
        return cipher_text, enc_session_key

    def decrypt_message(
            self, cipher_text: bytes, enc_session_key: bytes
    ) -> bytes:
        session_key = utils.decrypt_session_key_with_private_key(
            enc_session_key, self.__private_key, self.__user_passphrase
        )
        plain_text = utils.decrypt_message_with_session_key(
            cipher_text, session_key
        )
        return plain_text


if __name__ == "__main__":
    context = EncryptionContext(
        is_new_user=True,
        user_passphrase="password",
        username="test")
    public_key = context.public_key
    context2 = EncryptionContext(
        is_new_user=False,
        user_passphrase="password",
        username="test",
        user_public_key=public_key)
    print(f"public key: {context2.public_key}")
    print(f"username: {context2.username}")
    message = b"hello world"
    cipher_text, enc_session_key = context.encrypt_message(message=message,
                                                           receiver_public_key=context2.public_key)
    print(f"cipher text: {cipher_text}\nenc session key: {enc_session_key}")
    plain_text = context2.decrypt_message(cipher_text=cipher_text, enc_session_key=enc_session_key)
    print(f"plain text: {plain_text}")
