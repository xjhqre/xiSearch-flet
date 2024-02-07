import numpy as np
from lda import LDA

# 假设原始数据为data，shape为(1, 2048)
data = np.random.rand(1, 2048)

# 将数据类型转换为int64
data = data.astype('int64')

# 初始化LDA模型，设置降维后的维度为1024
model = LDA(n_topics=1024)

# 训练LDA模型并降维
model.fit(data)
new_data = model.transform(data)

# 输出降维后的数据，shape为(1, 1024)
print(new_data.shape)
