from typing import Optional, List
import logging
from db.database import DB
from encryption.encryption_context import EncryptionContext
from psycopg2.errors import UniqueViolation
from dataclasses import dataclass
import uuid
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)


@dataclass
class UserContext:
    username: Optional[str] = None
    enc_context: Optional[EncryptionContext] = None


@dataclass
class UserMessage:
    from_user: str
    to_user: str
    send_at: datetime
    file_uuid: str
    file_type: str
    session_key: str


class ApplicationContext:
    def __init__(self):
        self.__user_context = None
        self.__db = DB()

    def register(self, username, password):
        """
        Register a new user and create public and private keys.
        :param username:
        :param password:
        :return:
        """
        try:
            hashed_password = EncryptionContext.hash_password(password)
            self.__db.add_user(username, hashed_password)
            enc_context = EncryptionContext(
                is_new_user=True, username=username, user_passphrase=password
            )
            self.__user_context = UserContext(username, enc_context)
            self.__db.add_user_public_key(
                username, enc_context.public_key.decode("utf-8")
            )
            logging.info("User {} registered successfully".format(username))
        except UniqueViolation as e:
            pass

    def login(self, username, password):
        username, hashed_password = self.__db.get_user_by_username(username)[0]
        if username is None:
            logging.info("User {} does not exist".format(username))
            return
        if not EncryptionContext.check_password(password, hashed_password):
            logging.info("Password for user {} is incorrect".format(username))
            return
        public_key = self.__db.get_user_public_key(username)[0][0]
        enc_context = EncryptionContext(
            is_new_user=False,
            user_passphrase=password,
            username=username,
            user_public_key=public_key.encode("utf-8"),
        )
        self.__user_context = UserContext(username, enc_context)
        logging.info("User {} logged in successfully".format(username))

    def send_message(self, to_user, file, file_type):
        if self.__user_context is None:
            logging.info("User is not logged in")
            return
        receiver_public_key = self.__db.get_user_public_key(to_user)[0][0]
        if receiver_public_key is None:
            logging.info("User {} does not exist".format(to_user))
            return
        cipher_text, session_key = self.__user_context.enc_context.encrypt_message(
            message=file, receiver_public_key=receiver_public_key
        )
        file_uuid = str(uuid.uuid4())
        self._save_file(cipher_text, file_uuid)
        self.__db.send_user_message(
            from_user=self.__user_context.username,
            to_user=to_user,
            message_uuid=file_uuid,
            session_key=session_key,
            file_type=file_type,
        )
        logging.info("Message sent successfully")

    def get_messages(self):
        if self.__user_context is None:
            logging.info("User is not logged in")
            return
        rows = self.__db.get_user_messages(self.__user_context.username)
        messages: List[UserMessage] = []
        for row in rows:
            m = UserMessage(
                from_user=self.__user_context.username,
                to_user=row[0],
                file_uuid=row[1],
                file_type=row[2],
                send_at=row[3],
                session_key=row[4],
            )
            messages.append(m)
            print(m)
        return messages

    def download_message(self, message_uuid, session_key):
        nonce, cipher_text = self._load_file(message_uuid)
        if cipher_text is None:
            logging.info("Message {} does not exist".format(message_uuid))
            return
        decrypted_message = self.__user_context.enc_context.decrypt_message(
            cipher_text=cipher_text, enc_session_key=session_key, cipher_nonce=nonce
        )
        logging.info("Message {} downloaded successfully".format(message_uuid))
        return decrypted_message

    @property
    def username(self):
        return self.__user_context.username

    def _save_file(self, cipher_text, file_uuid):
        path = os.path.dirname(__file__)
        with open(f"{path}/encryption/media/{file_uuid}.bin", "wb") as f:
            print(f"1: {len(cipher_text[0])}\n2: {len(cipher_text[1])}")
            [f.write(chunk) for chunk in cipher_text]

    def _load_file(self, message_uuid):
        path = os.path.dirname(__file__)
        with open(f"{path}/encryption/media/{message_uuid}.bin", "rb") as f:
            nonce = f.read(8)
            cipher_text = f.read()
            print(f"1: {len(cipher_text)}\n2: {len(nonce)}")
        return nonce, cipher_text

    @property
    def get_public_key(self):
        return self.__user_context.enc_context.public_key


if __name__ == "__main__":
    username = "test12"
    password = "test"
    app_context = ApplicationContext()
    # app_context.register(username=username, password=password)
    app_context.login(username, password)
    public_key = app_context.get_public_key
    enc_context = EncryptionContext(False, username, password, public_key)
    cipher, session_key = enc_context.encrypt_message(b"test", public_key)
    plain_text = enc_context.decrypt_message(cipher[0], cipher[1], session_key)
    print(cipher)
