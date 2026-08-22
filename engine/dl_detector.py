import os
import joblib
import numpy as np

class DeepLearningDetector:
    """
    Evaluates flow-based features using the Deep Learning model (LSTM/CNN/MLP architecture).
    Classifies traffic into: Normal, DoS, DDoS, PortScan, BruteForce.
    """
    CLASSES = ["Normal", "DoS", "DDoS", "PortScan", "BruteForce"]

    def __init__(self, model_dir):
        model_path = os.path.join(model_dir, "dl_flow_model.joblib")
        scaler_path = os.path.join(model_dir, "flow_scaler.joblib")

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.is_loaded = True
        else:
            self.model = None
            self.scaler = None
            self.is_loaded = False

    def predict(self, feature_vector):
        """
        Input: 2D numpy array of raw flow features (1, 12)
        Output: dict containing predicted_label, confidence, probabilities
        """
        if not self.is_loaded:
            return {"predicted_label": "Normal", "confidence": 1.0, "probabilities": {c: 0.2 for c in self.CLASSES}}

        scaled_vector = self.scaler.transform(feature_vector)
        pred_idx = self.model.predict(scaled_vector)[0]
        probs = self.model.predict_proba(scaled_vector)[0]

        predicted_label = self.CLASSES[pred_idx] if pred_idx < len(self.CLASSES) else "Normal"
        confidence = float(probs[pred_idx])

        prob_dict = {self.CLASSES[i]: float(probs[i]) for i in range(len(self.CLASSES))}

        return {
            "predicted_label": predicted_label,
            "confidence": confidence,
            "probabilities": prob_dict
        }
