from pathlib import Path
from typing import Any, Dict, List, Tuple
from datetime import datetime
import os
from PIL import Image
import json

class ImageSelector():
    def __init__(self) -> None:
        self.base_dir = None
        self.filtered_images: Dict[str, Any] = {}
        self.all_images: List[Path] = []
        self.base_date_range: Tuple[datetime, datetime] = ()
        self.filterd_date_range: Tuple[datetime, datetime] = ()

    def check_for_existing_config(self) -> bool:
        for file in self.dir_path.glob("*.itp"):
            with open(file) as fp:
                self.available_images = json.load(fp)

        if len(self.available_images) == 0:
            return False
        return True

    def load_images(self, dir_path: Path, max_setter = None, value_setter = None, get_progress_state = None):
        """Load the image files of the specified path.

        Parameters
        ----------
        dir_path : Path
            Path to the image directory.
        """
        image_files = []
        self.dir_path = Path(dir_path)
        self.available_images = {}
        if self.check_for_existing_config():
            return
        types = ["*.png", "*.heic", "*.jpg", "*.jpeg", "*.HEIC"]
        for type in types:
            image_files.extend(self.dir_path.rglob(type))
        
        if max_setter:
            max_setter(len(image_files))
        max_date = datetime(1996, 1, 1, 0, 0, 0)
        min_date = datetime.today()
        for i, image in enumerate(image_files):
            cur_date = self.get_image_creation_date(image)
            if cur_date < min_date:
                min_date = cur_date
            if cur_date > max_date:
                max_date = cur_date
            self.available_images[str(Path(image).relative_to(Path(dir_path)))] = {"date": str(cur_date)}
            if value_setter:
                value_setter(i)
            if get_progress_state and get_progress_state():
                print("Image exploration aboarted by user.")
                value_setter(len(image_files))
                return

        value_setter(len(image_files))
        self.base_date_range = (min_date, max_date)

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
            except:
                creation_timestamp = None

        if creation_timestamp:
            creation_date = datetime.strptime(creation_timestamp, "%Y:%m:%d %H:%M:%S")
        else:
            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        return creation_date

    def store_progress(self, file_path: Path):
        with open(str(file_path.with_suffix(".itsf")), 'w+') as fp:
            json.dump(self.available_images, fp)