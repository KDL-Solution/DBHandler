import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lmdb_handler import LMDBHandler
import cv2
import numpy as np
from tqdm.contrib.concurrent import process_map
from multiprocessing import Lock
import time

lock = Lock()
lmdb_data = LMDBHandler("lmdb_test", 'w')    
def generate_fake_data(idx):
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    annots = {"idx": idx, "label": f"label_{idx}"}
    return img, annots

def process(worker_idx):
    # 각 워커에서 받은 idx 처리
    img, annots = generate_fake_data(worker_idx)
    lock.acquire()
    idx = len(lmdb_data) + 1
    print(f"Worker {worker_idx} inserted data with idx {idx}")
    
    lmdb_data.put_data(img, annots, idx)
    lock.release()
    
if __name__ == "__main__":
    # 처리할 idx 리스트 (0부터 99까지)
    
    num_data = 1000  # 처리할 데이터 수
    idx_list = list(range(num_data))
    
    process_map(process, idx_list, max_workers=10, chunksize=1)