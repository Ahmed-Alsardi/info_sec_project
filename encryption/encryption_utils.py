from typing import Tuple

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class EncryptionUtils:
    @staticmethod
    def generate_session_key(key_length=16) -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def generate_public_private_keys(passphrase: str) -> Tuple[bytes, bytes]:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pub_key = key.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PublicFormat.SubjectPublicKeyInfo)
        pri_key = key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.PKCS8,
                                    encryption_algorithm=serialization.BestAvailableEncryption(
                                        password=passphrase.encode("utf-8")
                                    ))
        return pub_key, pri_key

    @staticmethod
    def encrypt_session_key_with_public_key(
            session_key: bytes, public_key: bytes
    ) -> bytes:
        pub_key = serialization.load_pem_public_key(data=public_key)
        return pub_key.encrypt(plaintext=session_key, padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))

    @staticmethod
    def decrypt_session_key_with_private_key(
            session_key: bytes, private_key: bytes, passphrase: str
    ) -> bytes:
        pri_key = serialization.load_pem_private_key(
            data=private_key,
            password=passphrase.encode("utf-8"),
        )
        return pri_key.decrypt(
            ciphertext=session_key,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def encrypt_message_with_session_key(
            message: bytes, session_key: bytes
    ) -> bytes:
        aes = Fernet(session_key)
        return aes.encrypt(message)

    @staticmethod
    def decrypt_message_with_session_key(
            cipher_text: bytes, session_key: bytes, nonce: bytes = None
    ) -> bytes:
        aes = Fernet(session_key)
        return aes.decrypt(cipher_text)

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
    encrypted_message = utils.encrypt_message_with_session_key(
        message, session_key
    )
    decrypted_message = utils.decrypt_message_with_session_key(
        encrypted_message, session_key
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
