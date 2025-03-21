import h5py
import numpy as np
import json
import cv2
from pathlib import Path

from .file_handler import FileHandler


class HDF5Handler(FileHandler):
    def __init__(
        self,
        db_path,
        mode="r",
        force=False,
        verbose=False,
        compression=None,
        compression_opts=None,
        **kwargs,
    ):
        self.db_path = Path(db_path)
        self.verbose = verbose
        self.mode = mode

        if not str(db_path).endswith(".hdf5"):
            raise ValueError(
                f"Invalid file extension: '{self.db_path}'. Use '.hdf5' extension."
            )

        if mode == "r":
            if not self.db_path.exists():
                raise FileNotFoundError(f"{self.db_path} does not exist.")
            self.file = h5py.File(self.db_path, "r", libver="latest", swmr=True, **kwargs)

            if verbose:
                print(f"{self.db_path} opened in READ-ONLY mode")
        elif mode == "w":
            if self.db_path.exists():
                if not force:
                    raise FileExistsError(
                        f"{self.db_path} already exists. Use force=True to overwrite."
                    )
                self.db_path.unlink()

            self.file = h5py.File(self.db_path, "w", **kwargs)
            self.dtui8 = h5py.special_dtype(vlen=np.dtype("uint8"))
            self.utf8 = h5py.string_dtype(encoding="utf-8")

            self.file.create_dataset(
                "images",
                (0,),
                dtype=self.dtui8,
                maxshape=(None,),
                compression=compression,
                compression_opts=compression_opts,
            )
            self.file.create_dataset(
                "labels",
                (0,),
                dtype=self.utf8,
                maxshape=(None,),
                compression=compression,
                compression_opts=compression_opts,
            )

            if verbose:
                print(f"Created {self.db_path} in WRITE mode")

        elif mode == "a":
            self.file = h5py.File(self.db_path, "a", **kwargs)
            if verbose:
                print(f"{self.db_path} opened in APPEND mode")
        else:
            raise ValueError(
                f"Invalid mode: '{mode}'. Use 'r' for read-only, 'w' for write, 'a' for append."
            )

        self.images = self.file["images"]
        self.labels = self.file["labels"]

    def put_data(self, img, annots, idx):
        success, img_buffer = cv2.imencode(".jpg", img)
        if not success:
            raise ValueError(f"Failed to encode image at index {idx}")
        self._resize_datasets(idx + 1)

        self.images[idx] = img_buffer
        self.labels[idx] = json.dumps(annots, ensure_ascii=False)
        if self.verbose:
            print(f"Data {idx} added to {self.db_path}")

    def get_data(self, idx):
        img = cv2.imdecode(self.images[idx], cv2.IMREAD_COLOR)
        label = json.loads(self.labels[idx])
        return img, label

    def _resize_datasets(self, new_size):
        self.images.resize((new_size,))
        self.labels.resize((new_size,))

    def get_length(self):
        return len(self.images)

    def __len__(self):
        return self.get_length()

    def close(self):
        self.file.close()
        if self.verbose:
            print(f"Closed {self.db_path}")

    def __del__(self):
        if hasattr(self, "file") and self.file is not None:
            self.file.close()
            if self.verbose:
                print(f"{self.db_path} closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
