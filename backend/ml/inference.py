import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import os
import tensorflow as tf

# Suppress TensorFlow batch norm deprecation warning
import warnings
warnings.filterwarnings('ignore', message='.*_batch_norm.*')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Monkey patch to bypass 'groups' issue in Keras 3 with older models
from tensorflow.keras.layers import DepthwiseConv2D
_original_depthwise_init = DepthwiseConv2D.__init__

def _new_depthwise_init(self, *args, **kwargs):
    if 'groups' in kwargs:
        kwargs.pop('groups')
    _original_depthwise_init(self, *args, **kwargs)

DepthwiseConv2D.__init__ = _new_depthwise_init

# Path to trained model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "chilli_mobilenet.h5"
)

# Load model ONCE
model = load_model(MODEL_PATH)

IMG_SIZE = (224, 224)

def preprocess_image(image_bytes):
    """
    Convert raw image bytes to model-ready numpy array
    """
    img = Image.open(image_bytes).convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict(image_array):
    """
    Run model prediction
    """
    preds = model.predict(image_array)
    class_index = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))
    return class_index, confidence