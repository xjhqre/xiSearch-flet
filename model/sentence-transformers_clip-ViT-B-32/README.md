---
pipeline_tag: sentence-similarity
tags:
- sentence-transformers
- feature-extraction
- sentence-similarity
---

# clip-ViT-B-32

This is the Image & Text model [CLIP](https://arxiv.org/abs/2103.00020), which maps text and images to a shared vector space. For applications of the models, have a look in our documentation [SBERT.net - Image Search](https://www.sbert.net/examples/applications/image-search/README.html)

## Usage

After installing [sentence-transformers](https://sbert.net) (`pip install sentence-transformers`), the usage of this model is easy:

  
```python
from sentence_transformers import SentenceTransformer, util
from PIL import Image

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')

#Encode an image:
img_emb = model.encode(Image.open('two_dogs_in_snow.jpg'))

#Encode text descriptions
text_emb = model.encode(['Two dogs in the snow', 'A cat on a table', 'A picture of London at night'])

#Compute cosine similarities 
cos_scores = util.cos_sim(img_emb, text_emb)
print(cos_scores)
```

See our [SBERT.net - Image Search](https://www.sbert.net/examples/applications/image-search/README.html) documentation for more examples how the model can be used for image search, zero-shot image classification, image clustering and image deduplication.

## Performance

In the following table we find the zero-shot ImageNet validation set accuracy:

| Model | Top 1 Performance |
| --- | :---: |
| [clip-ViT-B-32](https://huggingface.co/sentence-transformers/clip-ViT-B-32) | 63.3 |
| [clip-ViT-B-16](https://huggingface.co/sentence-transformers/clip-ViT-B-16) | 68.1 |
| [clip-ViT-L-14](https://huggingface.co/sentence-transformers/clip-ViT-L-14) | 75.4 |

For a multilingual version of the CLIP model for 50+ languages have a look at: [clip-ViT-B-32-multilingual-v1](https://huggingface.co/sentence-transformers/clip-ViT-B-32-multilingual-v1)