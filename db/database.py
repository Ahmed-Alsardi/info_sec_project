import logging

import psycopg2
from psycopg2.errors import UniqueViolation, InFailedSqlTransaction

logging.basicConfig(level=logging.INFO)


class DB:
    def __init__(
            self,
            db_name="infosec",
            db_user="infosec",
            db_password="infosec",
        db_host="localhost",
        db_port=5435,
    ):
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
        except Exception as e:
            logging.error(e)
            raise e
        # Create Schema
        logging.info("connection to DB")
        self._create_schema()
        logging.info("schema created")

    def _create_schema(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS app_users(
                    username varchar(63) PRIMARY KEY NOT NULL,
                    password varchar(512) NOT NULL)"""
            )
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS app_public_keys(
            username varchar(63) NOT NULL PRIMARY KEY,
            public_key varchar(2048) NOT NULL,
            FOREIGN KEY (username) REFERENCES app_users(username))
            """
            )
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS app_messages(
            id serial PRIMARY KEY NOT NULL,
            to_user varchar(63) NOT NULL,
            from_user varchar(63) NOT NULL,
            send_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            session_key BYTEA NOT NULL,
            file BYTEA NOT NULL,
            file_name BYTEA NOT NULL,
            FOREIGN KEY (to_user) REFERENCES app_users(username),
            FOREIGN KEY (from_user) REFERENCES app_users(username))
            """
            )

    def add_user(self, username, password):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO app_users(username, password) VALUES(%s, %s)",
                    (username, password),
                )
            self.conn.commit()
            return True
        except UniqueViolation:
            logging.error("user already exists")
            return False
        except InFailedSqlTransaction as e:
            logging.error(e)
            logging.error("Fail Transaction")
            self.conn.rollback()
            return False

    def get_user_by_username(self, username):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT username, password FROM app_users WHERE username = %s",
                (username,),
            )
            return cur.fetchall()

    def add_user_public_key(self, username, public_key):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO app_public_keys(username, public_key) VALUES(%s, %s)",
                (username, public_key),
            )
        self.conn.commit()

    def get_user_public_key(self, username):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT public_key FROM app_public_keys WHERE username = %s",
                (username,),
            )
            return cur.fetchall()

    def send_user_message(
            self, from_user, file_name, to_user, session_key, file,
    ):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO app_messages(from_user, file_name, to_user, session_key, file)
                VALUES(%s, %s, %s, %s, %s)""",
                (from_user, file_name, to_user, session_key, file),

            )
        self.conn.commit()

    def get_user_messages(self, username):
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT 
                from_user, id, file_name, send_at, session_key FROM app_messages WHERE to_user = %s""",
                (username,),
            )
            return cur.fetchall()

    def get_message_by_id(self, message_id):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT file, session_key, file_name FROM app_messages WHERE id = %s
            """, (message_id,))
            return cur.fetchone()

    def get_users(self, except_user):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT username FROM app_users WHERE username != %s
            """, (except_user,))
            return cur.fetchall()


if __name__ == "__main__":
    db = DB("infosec", "infosec", "infosec", "localhost", 5435)
