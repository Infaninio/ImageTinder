import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from image_selector import SelectorImage


class TestSelectorImage(unittest.TestCase):
    """Test the selector image class."""

    def __init__(self, methodName: str = "Test SelectorImage class") -> None:
        """Set up Testclass."""
        super().__init__(methodName)
        self.default_date = datetime.today()

    def _creation_date_mock(self, path) -> datetime:
        return self.default_date

    @patch("image_selector.SelectorImage.get_image_creation_date")
    def test_constructors(self, creation_date_mock: MagicMock):
        creation_date_mock.side_effect = self._creation_date_mock

        test_creation = SelectorImage(Path("a/file/path.jpg"))
        self.assertEqual(test_creation.date, self.default_date)
        self.assertDictEqual(test_creation._reviews, {})
        self.assertEqual(test_creation._path, Path("a/file/path.jpg"))
        creation_date_mock.assert_called()
        json_content = {
            "creation_date": datetime(2023, 1, 23).isoformat(),
            "reviews": {"user1": False, "user2": 3.3},
        }

        test_creation = SelectorImage.from_json(
            Path("a/file/path.jpg"), json_content=json_content
        )
        self.assertEqual(test_creation.date, datetime(2023, 1, 23))
        self.assertEqual(test_creation._path, Path("a/file/path.jpg"))
        self.assertDictEqual(test_creation._reviews, {"user1": False, "user2": 3.3})

    @patch("image_selector.SelectorImage.get_image_creation_date")
    def test_json_creation(self, creation_date_mock: MagicMock):
        creation_date_mock.side_effect = self._creation_date_mock
        json_content = {
            "creation_date": datetime(2023, 1, 23).isoformat(),
            "reviews": {"user1": False, "user2": 3.3},
        }
        test_creation = SelectorImage.from_json(
            Path("a/file/path.jpg"), json_content=json_content
        )
        expected_result = {
            "a/file/path.jpg": {
                "creation_date": datetime(2023, 1, 23).isoformat(),
                "reviews": {"user1": False, "user2": 3.3},
            }
        }
        self.assertDictEqual(test_creation.to_json(), expected_result)

        json_content = {"creation_date": datetime(2023, 1, 23).isoformat()}
        test_creation = SelectorImage.from_json(
            Path("a/file/path.jpg"), json_content=json_content
        )
        expected_result = {
            "a/file/path.jpg": {
                "creation_date": datetime(2023, 1, 23).isoformat(),
                "reviews": {},
            }
        }
        self.assertDictEqual(test_creation.to_json(), expected_result)

    @patch("image_selector.SelectorImage.get_image_creation_date")
    def test_review_handling(self, creation_date_mock: MagicMock):
        creation_date_mock.side_effect = self._creation_date_mock
        json_content = {
            "creation_date": datetime(2023, 1, 23).isoformat(),
            "reviews": {"user1": False, "user2": 3.3},
        }
        test_creation = SelectorImage.from_json(
            Path("a/file/path.jpg"), json_content=json_content
        )
        test_creation.set_review("user1", True)
        test_creation.set_review("user3", 10)
        expected_result = {
            "a/file/path.jpg": {
                "creation_date": datetime(2023, 1, 23).isoformat(),
                "reviews": {"user1": True, "user2": 3.3, "user3": 10},
            }
        }
        self.assertDictEqual(test_creation.to_json(), expected_result)
        self.assertEqual(None, test_creation.get_review("user4"))
        self.assertEqual(3.3, test_creation.get_review("user2"))


if __name__ == "__main__":
    unittest.main()
