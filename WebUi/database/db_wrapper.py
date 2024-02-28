from typing import Any, Dict, List

import mariadb


class UserNotExisting(Exception):
    """Exception for non existing user."""

    pass


class UserAlreadyExists(Exception):
    """Exception for already existing user."""

    pass


class ImageTinderDatabase:
    """Wrapper for the ImageTinder Database to be easy usable from outside."""

    def __init__(
        self,
        user: str = "ImageTinderApp",
        password: str = "password",
        host: str = "localhost",
        port: int = 3306,
    ) -> None:
        """Create the database wrapper.

        Parameters
        ----------
        user : str, optional
            user for the database, by default "ImageTinderApp"
        password : str, optional
            password for the specific user, by default "password"
        host : str, optional
            host ip, by default "localhost"
        port : int, optional
            port for the database, by default 3306
        """
        self.connection = mariadb.connect(
            user=user, password=password, host=host, port=port
        )
        with self.connection.cursor() as cur:
            cur.execute("USE ImageTinder")

    def _execute_sql(self, statement: str, arguments: Dict[str, Any]) -> List[Any]:
        with self.connection.cursor() as cur:
            cur.execute(statement, arguments)
            return list(cur)

    def check_user_password(self, username: str, password_hash: str) -> bool:
        query = "SELECT password FROM user WHERE user.email = %(username);"
        result = self._execute_sql(query, {"username": username})
        if not result:
            raise UserNotExisting

        if result[0] == password_hash:
            return True
        else:
            return False

    def create_user(self, username: str, password_hash: str):
        query = "SELECT password FROM user WHERE user.email = %(username);"
        result = self._execute_sql(query, {"username": username})
        if result:
            raise UserAlreadyExists

        query = (
            "INSERT INTO user (email, password) VALUES (%(username), %(password_hash));"
        )
        self._execute_sql(query, {"username": username, "password_hash": password_hash})
