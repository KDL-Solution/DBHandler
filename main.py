from glob import glob
from upload import LMDBUploader
images = sorted(glob('data/biz_card_data/rebuild/images/*.jpg'))
labels = sorted(glob('data/biz_card_data/rebuild/labels/*.json'))

datalist = list(zip(images, labels))

uploader = LMDBUploader("data/lmdb/biz_card", max_workers=30, verbose=False)
uploader.upload(datalist)