import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

from PIL import Image


class SelectorImage:
    """Simple class to store custom metadata of a image."""

    def __init__(self, path: Path):
        """Create Image with metainformation.

        Parameters
        ----------
        path : Path
            Path to the image.
        """
        self._path: Path = path
        self._date: datetime = self.get_image_creation_date(path)
        self._reviews: Dict[str, Any] = {}

    def __hash__(self) -> int:
        """Hash the image."""
        hash(self._path)

    def __lt__(self, other):
        """Compare if less then other object."""
        return self._date < other._date

    def __eq__(self, __value: object) -> bool:
        """Compare if two objects are equal."""
        return self._path == __value._path

    @staticmethod
    def get_image_creation_date(file_path: Path) -> datetime:

        with Image.open(file_path) as img:
            # Get the creation timestamp from the image's Exif data
            try:
                exif_info = img._getexif()
                if exif_info and 36867 in exif_info:
                    creation_timestamp = exif_info[36867]
                else:
                    creation_timestamp = None
            except:  # noqa
                creation_timestamp = None

        if creation_timestamp:
            creation_date = datetime.strptime(creation_timestamp, "%Y:%m:%d %H:%M:%S")
        else:
            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        return creation_date

    def to_json(self, base_path: Optional[Path] = None) -> Dict[str, Any]:
        path = (
            self._path.relative_to(base_path.parent).as_posix()
            if base_path
            else self._path.as_posix()
        )
        result = {path: {"creation_date": self.date.isoformat()}}
        result[path]["reviews"] = self._reviews

        return result

    @classmethod
    def from_json(cls, file_path: Union[str, Path], json_content: Dict[str, Any]):
        image = cls(Path(file_path))
        image.date = json_content["creation_date"]
        for key, value in json_content.get("reviews", {}).items():
            image._reviews[key] = value
        return image

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, date: str):
        self._date = datetime.fromisoformat(date)

    def get_review(self, user: str) -> Optional[Any]:
        return self._reviews.get(user, None)

    def set_review(self, user: str, review: Any):
        self._reviews[user] = review


class ImageSelector:
    """Util to select/review images."""

    def __init__(self):
        """Set up Image Selector."""
        self._filtered_images: Dict[Path, SelectorImage] = {}
        self._base_date_range: Tuple[datetime, datetime] = ()
        self._filterd_date_range: Tuple[datetime, datetime] = ()
        self._current_user: Optional[Any] = None

    def load_images(
        self,
        dir_path: Path,
        max_setter=None,
        value_setter=None,
        get_progress_state=None,
    ):
        """Load the image files of the specified path.

        Parameters
        ----------
        dir_path : Path
            Path to the image directory.
        max_setter : _type_, optional
            Function to the max setter function of the ui/progress_bar, by default None
        value_setter : _type_, optional
            Function to the value setter function of the ui/progress_bar, by default None
        get_progress_state : _type_, optional
            Function to check if the user aboarted on the ui, by default None
        """
        image_files = []
        self._filtered_images = {}
        types = ["*.png", "*.heic", "*.jpg", "*.jpeg", "*.HEIC"]
        for type in types:
            image_files.extend(dir_path.rglob(type))

        if max_setter:
            max_setter(len(image_files))
        max_date = datetime(1996, 1, 1, 0, 0, 0)
        min_date = datetime.today()
        for i, image in enumerate(image_files):
            new_image = SelectorImage(image)
            if new_image.date < min_date:
                min_date = new_image.date
            if new_image.date > max_date:
                max_date = new_image.date
            self._filtered_images[image] = new_image
            if value_setter:
                value_setter(i)
            if get_progress_state and get_progress_state():
                print("Image exploration aboarted by user.")
                if value_setter:
                    value_setter(len(image_files))
                return
        if value_setter:
            value_setter(len(image_files))
        self._base_date_range = (min_date, max_date)

    def apply_date_filter(self, start_date: datetime, end_date: datetime):
        self._filterd_date_range = (start_date, end_date)
        for key in list(self._filtered_images.keys()):
            if not (
                start_date <= self._filtered_images[key].date
                and self._filtered_images[key].date <= end_date
            ):
                self._filtered_images.pop(key)

    def store_progress(self, file_path: Path, absolute: bool = False):

        vaiable_dict = {
            "start_date": self._filterd_date_range[0].isoformat(),
            "end_date": self._filterd_date_range[1].isoformat(),
            "images": {},
        }

        for _, value in self._filtered_images.items():
            if absolute:
                vaiable_dict["images"].update(value.to_json())
            else:
                vaiable_dict["images"].update(value.to_json(file_path))

        with open(str(file_path.with_suffix(".itsf")), "w+") as fp:
            json.dump(vaiable_dict, fp)

    def load_configuration(self, file_path: Path):
        with open(str(file_path), "r") as fp:
            json_data = json.load(fp)
        self._filterd_date_range = (
            datetime.fromisoformat(json_data["start_date"]),
            datetime.fromisoformat(json_data["end_date"]),
        )

        for key, value in json_data["images"].items():
            image_path = (
                Path(key) if Path(key).is_absolute() else Path(file_path.parent, key)
            )
            self._filtered_images[image_path] = SelectorImage.from_json(
                image_path, value
            )

    @property
    def user(self) -> Any:
        return self._current_user

    @user.setter
    def user(self, user: Any):
        self._current_user = user

    def get_next_image(self) -> Optional[Path]:
        if self._current_user is None:
            raise AttributeError(
                "The user Attribute is not set, set with object.user = 'Test'"
            )
        for img in sorted(self._filtered_images.values()):
            if img._reviews.get(self._current_user, None) is None:
                return img._path

        return None

    def __iter__(self):
        """Iterate through all images, filter by user.

        Yields
        ------
        Iterator[Path]
            Path to the next ImageFile

        Raises
        ------
        AttributeError
            If the user is not set, it can't be filtered.
        """
        if self._current_user is None:
            raise AttributeError(
                "The user Attribute is not set, set with object.user = 'Test'"
            )
        for img in sorted(self._filtered_images.values()):
            if img._reviews.get(self._current_user, None) is None:
                yield img._path

    def set_review(self, path: Path, value: Union[float, bool]):
        self._filtered_images[path]._reviews[self._current_user] = value
