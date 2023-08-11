import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

torch.set_num_threads(4)

model = SentenceTransformer('clip-ViT-B-32')


# 提取特征方法
def extract(img_path):
    img = Image.open(img_path)
    emb = model.encode([img], batch_size=1, convert_to_tensor=True, show_progress_bar=False)
    img.close()
    return emb
