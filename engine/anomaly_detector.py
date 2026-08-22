import os
import joblib
import numpy as np

class AnomalyDetector:
    """
    Protocol-Level Machine Learning Anomaly Detector (Random Forest).
    Monitors IP-MAC binding changes, gratuitous ARP reply rates, and conflict counts
    to identify low-volume ARP Spoofing / MITM attacks.
    """
    CLASSES = ["Normal ARP", "ARP Spoofing / MITM"]

    def __init__(self, model_dir):
        model_path = os.path.join(model_dir, "rf_arp_model.joblib")
        scaler_path = os.path.join(model_dir, "arp_scaler.joblib")

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.is_loaded = True
        else:
            self.model = None
            self.scaler = None
            self.is_loaded = False

    def predict(self, arp_vector):
        """
        Input: 2D numpy array of ARP protocol metrics (1, 5)
        Output: dict containing is_anomaly, predicted_label, confidence, probability
        """
        if not self.is_loaded:
            return {"is_anomaly": False, "predicted_label": "Normal ARP", "confidence": 1.0, "anomaly_score": 0.0}

        scaled_vector = self.scaler.transform(arp_vector)
        pred_idx = self.model.predict(scaled_vector)[0]
        probs = self.model.predict_proba(scaled_vector)[0]

        is_anomaly = bool(pred_idx == 1)
        predicted_label = self.CLASSES[pred_idx]
        confidence = float(probs[pred_idx])
        anomaly_score = float(probs[1])

        return {
            "is_anomaly": is_anomaly,
            "predicted_label": predicted_label,
            "confidence": confidence,
            "anomaly_score": anomaly_score
        }
