import os
import cv2
import json
from multiprocessing import Pool, Lock
from lmdb_handler import LMDBHandler
from typing import List
from tqdm import tqdm

# Pool의 initializer에서 호출할 초기화 함수
lock = None
lmdb_data = None
def init(l, lmdb):
    global lock
    global lmdb_data
    lock = l
    lmdb_data = lmdb

class LMDBUploader:
    def __init__(self, lmdb_path, max_workers=10, verbose=False):
        # LMDB 핸들러와 멀티프로세싱 락 생성
        if os.path.exists(lmdb_path):
            raise FileExistsError(f"{lmdb_path} already exists.")
        self.lmdb_data = LMDBHandler(lmdb_path, mode='w', verbose=verbose)
        self.lock = Lock()
        self.max_workers = max_workers
        self.verbose = verbose
        
    @staticmethod
    def process(data_pair):
        
        global lock, lmdb_data
        if lock is None or lmdb_data is None:
            raise ValueError("Initializer not called.")
        img_path, label_path = data_pair
        
        # 이미지 읽기
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Failed to read image {img_path}")
            return

        # 라벨 읽기
        try:
            with open(label_path, 'r', encoding='utf-8') as f:
                annots = json.load(f)
        except FileNotFoundError:
            print(f"Error: Label file not found {label_path}")
            return

        with lock:
            idx = len(lmdb_data) + 1  # 새로운 인덱스
            lmdb_data.put_data(img, annots, idx)
        
    def upload(self, data_pairs):
        
        # Pool을 사용하여 멀티프로세싱 처리
        with Pool(processes=self.max_workers, initializer=init, initargs=(self.lock, self.lmdb_data)) as pool:
            for _ in tqdm(pool.imap(self.process, data_pairs), total=len(data_pairs)):
                pass

        
if __name__ == "__main__":
    # 이미지와 라벨 경로
    data_pairs = [
        ["example/data/images/image_000000.jpg", "example/data/labels/image_000000.json"],
        ["example/data/images/image_000001.jpg", "example/data/labels/image_000001.json"],
        ["example/data/images/image_000002.jpg", "example/data/labels/image_000002.json"],
    ]
    
    # LMDB 업로더 생성
    uploader = LMDBUploader("lmdb_test",max_workers=10, verbose=True)
    
    # 업로드 실행
    uploader.upload(data_pairs)

        