# LMDB Handler

This repository provides a simple utility for handling LMDB databases with images and annotations. You can store and retrieve images and their corresponding annotations efficiently using this handler.

## Features

- Store and retrieve images with annotations in an LMDB database.
- Easy-to-use functions for saving and loading data.
- Supports encoding images using `cv2` to save space.
- **LMDBUploader** : Multiprocessing support for efficient data insertion

## Installation

1. Clone the repository:

```bash
git clone https://github.com/KDL-Solution/LMDB_Handler
cd LMDB_Handler
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

# Usage
<details>
<summary>
 <font size="+1">LMDBUploader</font>
</summary>

</details>


How to Use 


## LMDBUploader 

```python
from upload import LMDBUploader
# 이미지와 라벨 경로
data_pairs = [
    ("./data/img1.jpg", "./data/label1.json"),
    ("./data/img2.jpg", "./data/label2.json"),
    ("./data/img3.jpg", "./data/label3.json"),
    ("./data/img4.jpg", "./data/label4.json"),
    ("./data/img5.jpg", "./data/label5.json"),
]

# LMDB 업로더 생성
uploader = LMDBUploader("lmdb_test", mode='w', max_workers=10, verbose=True)

# 업로드 실행
uploader.upload(data_pairs)