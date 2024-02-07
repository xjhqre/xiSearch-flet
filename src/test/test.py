import numpy as np
from sklearn.decomposition import PCA

# 创建一维数组
x = np.array([1, 2, 3, 4, 5])

# 将一维数组转换为二维数组
X = x.reshape(-1, 1)
print(X)
# 创建 PCA 模型
pca = PCA(n_components=2)

# 对数据进行降维
X_pca = pca.fit_transform(X)

# 输出降维后的结果
print(X_pca)
