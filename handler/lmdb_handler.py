import lmdb
import os
import cv2
import json
import shutil
import numpy as np
from pathlib import Path
from .file_handler import FileHandler

LMDB_MAP_SIZE = 10 * 1024**4  # 10 TiB


def encode(string_data):
    return string_data.encode("utf-8")


def decode(string_data):
    return string_data.decode("utf-8")


class LMDBHandler(FileHandler):
    def __init__(self, db_path, mode="r", force=False, verbose=False, max_readers=512):
        self.db_path = Path(db_path).resolve()
        self.verbose = verbose
        self.mode = mode
        
        if mode == "r":
            if not self.db_path.exists():
                raise FileNotFoundError(f"{self.db_path} does not exist.")
            self.env = lmdb.open(self.db_path,
                                 readonly=True,
                                 lock=False,
                                 readahead=False,
                                 meminit=False,
                                 max_readers=max_readers)
            if verbose:
                print(f"{self.db_path} opened in READ-ONLY mode")
        elif mode == "w":
            if self.db_path.exists():
                if not force:
                    raise FileExistsError(f"{self.db_path} already exists. Use force=True to overwrite.")
                self.db_path.rmdir()
            self.db_path.mkdir(parents=True, exist_ok=True)
            self.env = lmdb.open(str(self.db_path),
                                 map_size=int(LMDB_MAP_SIZE),
                                 readonly=False,
                                 max_readers=max_readers,)
            
            if verbose:
                print(f"{self.db_path} opened in WRITE mode")
        elif mode == "a":
            self.db_path.mkdir(parents=True, exist_ok=True)
            self.env = lmdb.open(self.db_path, 
                                 readonly=False, 
                                 max_readers=max_readers)
            if verbose:
                print(f"{self.db_path} opened in APPEND mode")
        else:
            raise ValueError(f"Invalid mode: '{mode}'. Use 'r' for read-only, 'w' for write, 'a' for append.")

    def _get(self, key):
        with self.env.begin(write=False) as txn:
            value = txn.get(key)
        return value

    def _put(self, key, value):
        with self.env.begin(write=True) as txn:
            txn.put(key, value)

    def put_data(self, img, annots, idx):
        
        self._put_img(img, idx)
        self._put_annots(annots, idx)
        
        if self.verbose:
            print(f"Data {idx} inserted.")
            
        self.update_num_data()
        return idx

    def get_data(self, idx):
        img = self._get_img(idx)
        annots = self._get_annots(idx)
        return img, annots

    def _put_img(self, img, idx):
        success, img_buffer = cv2.imencode(".jpg", img)
        if success:
            self._put(encode(f"{idx}_img"), img_buffer.tobytes())
        else:
            raise Exception(f"Failed to encode image for index {idx}")

    def _put_annots(self, annots, idx):
        self._put(
            encode(f"{idx}_annots"), encode(json.dumps(annots, ensure_ascii=False))
        )

    def _get_img(self, idx):
        img_buffer = self._get(encode(f"{idx}_img"))
        if img_buffer is None:
            return KeyError(f"No image found for index {idx}")
        img_array = np.frombuffer(img_buffer, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img

    def _get_annots(self, idx):
        annots = self._get(encode(f"{idx}_annots"))
        if annots is None:
            raise KeyError(f"No annotation found for index {idx}")
        annots = json.loads(decode(annots))
        return annots

    def _get_num_data(self):
        num_data = self._get("num_data".encode())
        return int(decode(num_data)) if num_data else 0

    def _put_num_data(self, num_data):
        self._put(encode("num_data"), encode(str(num_data)))

    def get_length(self):
        with self.env.begin(write=False) as txn:
            return txn.stat()["entries"]
        
    def update_num_data(self):
        
        num_data = self.get_length() // 2
        self._put_num_data(num_data)
        if self.verbose:
            print(f"{self.db_path} updated. NUM_DATA: {self._get_num_data()}")
            
    def __len__(self):
        return self._get_num_data()
    
    def close(self):
        self.env.close()
        if self.verbose:
            print(f"Closed {self.db_path}")

    def __del__(self):
        if hasattr(self, "env") and self.env is not None:
            self.env.close()
            if self.verbose:
                print(f"{self.db_path} closed.")