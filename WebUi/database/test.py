import unittest
from pathlib import Path

import mariadb
from db_wrapper import ImageTinderDatabase as DB


class TestImageSelector(unittest.TestCase):
    """Test ImageSelector class."""

    def __init__(self, methodName: str = "Test SelectorImage class") -> None:
        """Set up Testclass."""
        super().__init__(methodName)
        connection = mariadb.connect(
            user="root",
            password="password",  # pragma: allowlist secret
            host="localhost",
            port=33061,
        )
        self.cursor = connection.cursor()
        self.set_up_database()

        self.db = DB(user="root", password="password", port=33061)

    def set_up_database(self):
        with open(Path(Path(__file__).parent.parent, "schema.sql")) as sql_file:
            data = sql_file.read().replace("\n", "").split(";")
            for query in data:
                if query:
                    self.cursor.execute(query)

        with open(Path(Path(__file__).parent, "fill_table.sql")) as sql_file:
            data = sql_file.read().replace("\n", "").split(";")
            for query in data:
                if query:
                    self.cursor.execute(query + ";")
        self.cursor.connection.commit()

    def test_create_user(self):
        pass


if __name__ == "__main__":
    unittest.main()
