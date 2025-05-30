import numpy as np
from PIL import Image
from scipy.stats import entropy as softmax_entropy
from skimage.measure import shannon_entropy

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_np = np.array(img)
    img_input = img_np / 255.0
    img_input = np.expand_dims(img_input, axis=0).astype(np.float32)
    return img_input, img_np

def is_uncertain(probabilities, threshold=0.7):
    return softmax_entropy(probabilities) > threshold

def is_low_entropy(img_np, threshold=4.0):
    return shannon_entropy(img_np) < threshold