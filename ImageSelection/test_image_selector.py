import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from image_selector import ImageSelector, SelectorImage


class TestImageSelector(unittest.TestCase):
    """Test ImageSelector class."""

    def __init__(self, methodName: str = "Test SelectorImage class") -> None:
        """Set up Testclass."""
        super().__init__(methodName)
        self.default_date = datetime.today()

    def set_up_example_config(self):
        pass

    def _creation_date_mock(self, path) -> datetime:
        for i in range(1, 20):
            if f"image{i}" == str(path):
                return datetime(2024, 2, i)

    @patch("image_selector.SelectorImage.get_image_creation_date")
    @patch("pathlib.Path.rglob")
    def test_load_images(
        self, path_rglob_patch: MagicMock, creation_date_mock: MagicMock
    ):
        path_rglob_patch.return_value = [f"image{i}" for i in range(1, 20)]
        creation_date_mock.side_effect = self._creation_date_mock
        test_object = ImageSelector()
        test_object.load_images(Path("/test/path"))
        for i in range(1, 20):
            self.assertIn(f"image{i}", test_object._filtered_images)
            self.assertIsInstance(
                test_object._filtered_images[f"image{i}"], SelectorImage
            )
            self.assertEqual(
                test_object._filtered_images[f"image{i}"].date, datetime(2024, 2, i)
            )

    @patch("image_selector.SelectorImage.get_image_creation_date")
    @patch("pathlib.Path.rglob")
    def test_filter_images(
        self, path_rglob_patch: MagicMock, creation_date_mock: MagicMock
    ):
        path_rglob_patch.return_value = [f"image{i}" for i in range(1, 20)]
        creation_date_mock.side_effect = self._creation_date_mock
        test_object = ImageSelector()
        test_object.load_images(Path("/test/path"))
        test_object.apply_date_filter(datetime(2024, 2, 5), datetime(2024, 2, 11))
        self.assertEqual(len(test_object._filtered_images), 7)


if __name__ == "__main__":
    unittest.main()
