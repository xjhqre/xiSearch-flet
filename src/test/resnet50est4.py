import numpy as np
from keras import Model
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing import image

model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model_output = Dense(1024, activation='relu')(model.output)
model = Model(model.input, model_output)

img = image.load_img("F:\\ACG\\新建文件夹\\63-1Z6261433432Y.jpg", target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
embeddings = model.predict(x)  # 执行图像嵌入
print(embeddings.flatten())
