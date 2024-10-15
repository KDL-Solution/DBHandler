import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lmdb_handler import LMDBHandler
import cv2
import numpy as np

lmdb_data = LMDBHandler("lmdb_test",'w')

img = np.zeros((512, 512, 3), dtype=np.uint8)
annotations = {"label": "example", "bbox": [100, 200, 300, 400]}
idx = lmdb_data.put_data(img, annotations,0)


lmdb_data = LMDBHandler("lmdb_test",'r')
img, annotations = lmdb_data.get_data(0)
print(len(lmdb_data))
print(img.shape)
print(annotations)

