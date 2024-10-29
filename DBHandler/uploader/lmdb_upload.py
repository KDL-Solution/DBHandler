import os
import cv2
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from DBHandler.handler.lmdb_handler import LMDBHandler


class LMDBUploader:
    def __init__(self, lmdb_path, max_workers=10, force=False, verbose=False):
        # LMDB 핸들러 초기화
        self.lmdb_data = LMDBHandler(lmdb_path, mode="w", force=force, verbose=verbose)
        self.max_workers = max_workers
        self.verbose = verbose

    @staticmethod
    def process(data_pair):
        img_path, label_path = data_pair

        # 이미지 읽기
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Failed to read image {img_path}")
            return None

        # 라벨 읽기
        try:
            with open(label_path, "r", encoding="utf-8") as f:
                annots = json.load(f)
        except FileNotFoundError:
            print(f"Error: Label file not found {label_path}")
            return None

        return img, annots

    def upload(self, data_pairs):
        # 멀티스레드로 데이터 가공 및 저장
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.process, data_pair) for data_pair in data_pairs
            ]
            for future in tqdm(as_completed(futures), total=len(futures)):
                data = future.result()
                if data is not None:
                    img, annots = data
                    idx = len(self.lmdb_data)
                    self.lmdb_data.put_data(img, annots, idx)

        # 모든 데이터 저장 후 LMDB 핸들러 닫기
        self.lmdb_data.close()


if __name__ == "__main__":
    # 예시 데이터 페어
    data_pairs = [
        [
            "example/data/images/image_000000.jpg",
            "example/data/labels/image_000000.json",
        ],
        [
            "example/data/images/image_000001.jpg",
            "example/data/labels/image_000001.json",
        ],
        [
            "example/data/images/image_000002.jpg",
            "example/data/labels/image_000002.json",
        ],
    ]

    # LMDB 업로더 생성
    uploader = LMDBUploader(r"lmdb_test", max_workers=10, force=True, verbose=True)

    # 업로드 실행
    uploader.upload(data_pairs)
