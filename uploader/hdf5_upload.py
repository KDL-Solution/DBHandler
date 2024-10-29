import cv2
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from handler import HDF5Handler


class HDF5Uploader:
    def __init__(self, hdf5_path, max_workers=10, force=False, verbose=False):
        # HDF5 핸들러 초기화
        self.hdf5_data = HDF5Handler(hdf5_path, mode="w", force=force, verbose=verbose)
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
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.process, data_pair) for data_pair in data_pairs
            ]
            for future in tqdm(as_completed(futures), total=len(futures)):
                data = future.result()
                if data is not None:
                    img, annots = data
                    idx = len(self.hdf5_data)
                    self.hdf5_data.put_data(img, annots, idx)
        self.hdf5_data.close()


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
    ] * 30

    # HDF5 업로더 생성
    uploader = HDF5Uploader(r"hdf5_test.hdf5", max_workers=10, force=True, verbose=True)

    # 업로드 실행
    uploader.upload(data_pairs)
