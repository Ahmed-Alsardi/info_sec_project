import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

class DB:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        try:
            self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        except Exception as e:
            logging.error(e)
            raise e
        # Create Schema
        logging.info("connection to DB")
        self._create_schema()

    def _create_schema(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS app_users(
                    username varchar(63) PRIMARY KEY NOT NULL,
                    password varchar(512) NOT NULL)""")
            cur.execute("""
            CREATE TABLE IF NOT EXISTS app_public_keys(
            username varchar(63) NOT NULL PRIMARY KEY,
            public_key varchar(2048) NOT NULL,
            FOREIGN KEY (username) REFERENCES app_users(username))
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS app_messages(
            id serial PRIMARY KEY NOT NULL,
            to_user varchar(63) NOT NULL,
            from_user varchar(63) NOT NULL,
            send_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            message BYTEA NOT NULL,
            session_key varchar(2048) NOT NULL,
            file_type VARCHAR(31) NOT NULL,
            FOREIGN KEY (to_user) REFERENCES app_users(username),
            FOREIGN KEY (from_user) REFERENCES app_users(username))
            """)


if __name__ == "__main__":
    db = DB("infosec", "infosec", "infosec", "localhost", "5435")
