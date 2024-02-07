import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image

model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

img = image.load_img("F:\\ACG\\新建文件夹\\63-1Z6261433432Y.jpg", target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
embeddings = model.predict(x)  # 执行图像嵌入
new_vector = np.reshape(embeddings, (1, 1024))
print(embeddings.flatten())  # (1, 2048)
print(new_vector.flatten())

if __name__ == '__main__':
    from sklearn.decomposition import PCA
    import numpy as np

    # 假设你的数据存储在一个名为data的numpy数组中，其形状为(1, 2048)
    data = np.random.rand(1, 2048)

    # 创建PCA对象并指定要降低到的维度
    pca = PCA(n_components=1024)

    # 对数据进行降维
    data_reduced = pca.fit_transform(data)

    # 输出降维后的数据形状
    print(data_reduced.shape)  # (1, 1024)
