from tensorflow.keras.preprocessing.image import ImagedataGenerator
import os

TRAIN_DIR ="../../data/Chilli/train"

gen= ImageDataGenerator(rescale=1./255)
flow = gen.flow_from_directory(TRAIN_DIR,
target_size=(224,224), batch_size=1)

print(flow.class_indices)