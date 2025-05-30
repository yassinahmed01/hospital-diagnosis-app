import json
import onnxruntime as ort

model_session = ort.InferenceSession("densenet121_model.onnx")

with open("class_names.json", "r") as f:
    class_labels = json.load(f)
