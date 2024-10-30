# DB Handler

This repository provides a simple utility for handling Databases(LMDB, HDF5) with images and annotations. You can store and retrieve images and their corresponding annotations efficiently using this handler.

## Features

- Store and retrieve images with annotations in database.
- Easy-to-use functions for saving and loading data.
- Supports encoding images using `cv2` to save space.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/KDL-Solution/FileHandler
cd FileHandler
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

# Usage
How to Use 

## Uploader 

```python
#from uploader import LMDBUploader as Uploader
from uploader import HDF5Uploader as Uploader
# 이미지와 라벨 경로
data_pairs = [
    ("./data/img1.jpg", "./data/label1.json"),
    ("./data/img2.jpg", "./data/label2.json"),
    ("./data/img3.jpg", "./data/label3.json"),
    ("./data/img4.jpg", "./data/label4.json"),
    ("./data/img5.jpg", "./data/label5.json"),
]

# 업로더 생성
uploader = Uploader("test", mode='w', max_workers=10, verbose=True)

# 실행
uploader.upload(data_pairs)
