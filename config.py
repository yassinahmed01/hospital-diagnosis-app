import os
import json
import onnxruntime as ort
from pytz import timezone

# Paths 
UPLOAD_FOLDER = 'static/uploads'
INSTANCE_FOLDER = os.path.join(os.getcwd(), 'instance')
MODEL_PATH = "densenet121_model.onnx"
CLASS_NAMES_PATH = "class_names.json"

#  Globals 
rejected_attempts = 0
egypt = timezone('Africa/Cairo')

# Model + Labels 
model_session = ort.InferenceSession(MODEL_PATH)
with open(CLASS_NAMES_PATH, "r") as f:
    class_labels = json.load(f)
