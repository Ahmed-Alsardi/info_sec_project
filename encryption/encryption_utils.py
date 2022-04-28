from typing import Tuple

from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import bcrypt


class EncryptionUtils:
    @staticmethod
    def generate_session_key(key_length=16) -> bytes:
        return get_random_bytes(key_length)

    @staticmethod
    def generate_public_private_keys(passphrase: str) -> Tuple[bytes, bytes]:
        key = RSA.generate(2048)
        public_key = key.public_key().exportKey()
        private_key = key.exportKey(
            passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC"
        )
        return public_key, private_key

    @staticmethod
    def encrypt_session_key_with_public_key(
        session_key: bytes, public_key: bytes
    ) -> bytes:
        public_key = RSA.importKey(public_key)
        cipher_rsa = PKCS1_OAEP.new(public_key)
        return cipher_rsa.encrypt(session_key)

    @staticmethod
    def decrypt_session_key_with_private_key(
        session_key: bytes, private_key: bytes, passphrase: str
    ) -> bytes:
        private_key = RSA.importKey(private_key, passphrase=passphrase)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        return cipher_rsa.decrypt(session_key)

    @staticmethod
    def encrypt_message_with_session_key(
        message: bytes, session_key: bytes
    ) -> Tuple[bytes, bytes]:
        cipher_aes = AES.new(session_key, AES.MODE_CTR)
        ciphertext = cipher_aes.encrypt(message)
        return cipher_aes.nonce, ciphertext

    @staticmethod
    def decrypt_message_with_session_key(
        cipher_text: bytes, session_key: bytes, nonce: bytes
    ) -> bytes:
        cipher_aes = AES.new(session_key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipher_aes.decrypt(cipher_text)
        return plaintext

    @staticmethod
    def hash_password(password: bytes) -> str:
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(password: bytes, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password, hashed_password)


if __name__ == "__main__":
    utils = EncryptionUtils()
    session_key = utils.generate_session_key()
    public_key, private_key = utils.generate_public_private_keys("password")
    encrypted_session_key = utils.encrypt_session_key_with_public_key(
        session_key, public_key
    )
    decrypted_session_key = utils.decrypt_session_key_with_private_key(
        encrypted_session_key, private_key, "password"
    )
    assert session_key == decrypted_session_key
    message = b"Hello World!"
    enc_nonce, encrypted_message = utils.encrypt_message_with_session_key(
        message, session_key
    )
    decrypted_message = utils.decrypt_message_with_session_key(
        encrypted_message, session_key, enc_nonce
    )
    assert message == decrypted_message
    print(f"session_key: {session_key}")
    print(f"encrypted_session_key: {encrypted_session_key}")
    print(f"decrypted_session_key: {decrypted_session_key}")
    print(f"message: {message}")
    print(f"encrypted_message: {encrypted_message}")
    print(f"decrypted_message: {decrypted_message}")
    print("Success!")

    password = b"password"
    hashed_password = utils.hash_password(password)
    assert utils.check_password(password, hashed_password.encode("utf-8"))
    print(f"password: {password}")
    print(f"hashed_password: {hashed_password}")
    print("Success!")
