from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from psycopg2.errors import UniqueViolation

from db.database import DB
from encryption.encryption_context import EncryptionContext

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
    file_id: int
    file_name: str


@dataclass
class DownloadUserMessage:
    file_id: int
    file_name: str
    file: bytes


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
            if not self.__db.add_user(username, hashed_password):
                logging.info("User {} already exists".format(username))
                return False
            enc_context = EncryptionContext(
                is_new_user=True, username=username, user_passphrase=password
            )
            self.__user_context = UserContext(username, enc_context)
            self.__db.add_user_public_key(
                username, enc_context.public_key.decode("utf-8")
            )
            logging.info("User {} registered successfully".format(username))
            return True
        except UniqueViolation as e:
            logging.error(e)
            return False

    def login(self, username, password):
        try:
            username, hashed_password = self.__db.get_user_by_username(username)[0]
            if username is None:
                logging.info("User {} does not exist".format(username))
                return False
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
            return True
        except Exception as e:
            logging.error(e)
            return False

    def send_message(self, to_user, file, file_name):
        if self.__user_context is None:
            logging.info("User is not logged in")
            return
        receiver_public_key = self.__db.get_user_public_key(to_user)[0][0]
        if receiver_public_key is None:
            logging.info("User {} does not exist".format(to_user))
            return
        cipher_text, session_key, file_name = self.__user_context.enc_context.encrypt_message(
            message=file, receiver_public_key=receiver_public_key, file_name=file_name
        )
        self.__db.send_user_message(
            from_user=self.__user_context.username,
            to_user=to_user,
            session_key=session_key,
            file_name=file_name,
            file=cipher_text
        )
        logging.info(f"Message sent from: {self.__user_context.username} to {to_user}")

    def get_messages(self) -> List[UserMessage] | None:
        if self.__user_context is None:
            logging.info("User is not logged in")
            return None
        rows = self.__db.get_user_messages(self.__user_context.username)
        messages: List[UserMessage] = []
        for row in rows:
            file_name = self._decrypt_file_name(name=bytes(row[2]), session_key=bytes(row[4]))
            m = UserMessage(
                to_user=self.__user_context.username,
                from_user=row[0],
                file_id=row[1],
                file_name=file_name,
                send_at=row[3],
            )
            messages.append(m)
        return messages

    def download_message(self, message_id) -> DownloadUserMessage | None:
        cipher_text, session_key, file_name = self.__db.get_message_by_id(message_id=message_id)
        if cipher_text is None:
            logging.info(f"Message with id {message_id} does not exist")
            return None
        decrypted_message = self.__user_context.enc_context.decrypt_message(
            cipher_text=bytes(cipher_text), enc_session_key=bytes(session_key)
        )
        file_name = self._decrypt_file_name(name=bytes(file_name),
                                            session_key=bytes(session_key))
        logging.info(f"Message with id {message_id} downloaded successfully")
        return DownloadUserMessage(file_name=file_name, file=decrypted_message, file_id=message_id)

    @property
    def username(self):
        return self.__user_context.username if self.__user_context else None

    @property
    def get_public_key(self):
        return self.__user_context.enc_context.public_key

    def get_users(self) -> List[str]:
        return [username[0] for username in self.__db.get_users(except_user=self.__user_context.username)]

    def logout(self):
        logging.info(f"User {self.__user_context.username} logged out")
        self.__user_context = None

    def _decrypt_file_name(self, name: bytes, session_key: bytes) -> str:
        return self.__user_context.enc_context.decrypt_message(cipher_text=name,
                                                               enc_session_key=session_key).decode("utf-8")


if __name__ == "__main__":
    username = "user1"
    username1 = "user2"
    password = "pass1"
    password1 = "pass2"
    app_context = ApplicationContext()
    # ========= Register users =========
    # app_context.register(username=username, password=password)
    # app_context.logout()
    # app_context.register(username=username1, password=password1)
    # ========== End of Register users ==========

    app_context.login(username=username, password=password)
    app_context.send_message(to_user=username1, file=b"Hello", file_name="text.txt")
    # logout
    app_context.logout()
    app_context.login(username=username1, password=password1)
    # print(f"equal: {session_key == app_context.get_messages()[0].session_key}")
    for m in app_context.get_messages():
        print(app_context.download_message(m.file_id))

    # app_context.logout()
    # for m in app_context.get_messages():
    #     d_message = app_context.download_message(m.file_uuid, m.session_key)
    #     print(d_message)
    # public_key = app_context.get_public_key
    # enc_context = EncryptionContext(False, username=username, user_passphrase=password, user_public_key=public_key)
    # cipher, session_key = enc_context.encrypt_message(b"test", public_key)
    # plain_text = enc_context.decrypt_message(cipher[0], cipher[1], session_key)
    # print(cipher)
    # print(plain_text)
