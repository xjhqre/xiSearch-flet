import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 原始向量
vector1 = np.array([1, 2, 3])
vectors_to_compare = [np.array([3, 4, 5]), np.array([2, 3, 4]), np.array([1, 0, 1])]

# print(type(vectors_to_compare))
# print(vectors_to_compare.shape)

# 计算余弦相似度
similarities = cosine_similarity([vector1], vectors_to_compare)

# 获取最相似的几个向量
num_similar_vectors = 2  # 想要获取最相似的几个向量
print(similarities.argsort())
most_similar_indices = similarities.argsort()[0][-num_similar_vectors:][::-1]
print(most_similar_indices.shape)
