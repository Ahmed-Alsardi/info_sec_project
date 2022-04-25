from typing import Optional
import logging
from db.database import DB
from encryption.encryption_context import EncryptionContext
from psycopg2.errors import UniqueViolation
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@dataclass
class UserContext:
    username: Optional[str] = None
    enc_context: Optional[EncryptionContext] = None


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
            enc_context = EncryptionContext(is_new_user=True,
                                            username=username,
                                            user_passphrase=password)
            self.__user_context = UserContext(username, enc_context)
            self.__db.add_user_public_key(username, enc_context.public_key)
            logging.info("User {} registered successfully".format(username))
        except UniqueViolation as e:
            pass

    def login(self, username, password):
        pass

    def send_message(self, to_user, file, file_type, ):
        pass

    def get_messages(self):
        pass
