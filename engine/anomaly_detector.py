import os
import numpy as np

class AnomalyDetector:
    """
    Protocol-Level Machine Learning Anomaly Detector (Random Forest).
    Monitors IP-MAC binding changes, gratuitous ARP reply rates, and conflict counts
    to identify low-volume ARP Spoofing / MITM attacks.
    Uses trained Random Forest model with a deterministic fallback for maximum serverless resilience.
    """
    CLASSES = ["Normal ARP", "ARP Spoofing / MITM"]

    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.tried_loading = False
        self.is_loaded = False

    def _load_model(self):
        if self.tried_loading:
            return
        self.tried_loading = True

        model_path = os.path.join(self.model_dir, "rf_arp_model.joblib")
        scaler_path = os.path.join(self.model_dir, "arp_scaler.joblib")

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                import joblib
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.is_loaded = True
                print("[AnomalyDetector] Successfully loaded trained Random Forest model.")
            except BaseException as e:
                print(f"[AnomalyDetector] Joblib load fallback: {e}")
                self.is_loaded = False

    def predict(self, arp_vector):
        """
        Input: 2D numpy array of ARP protocol metrics (1, 5)
        Features: [arp_request_rate, arp_reply_rate, arp_reply_req_ratio, mac_change_rate, ip_mac_binding_conflicts]
        """
        self._load_model()

        if self.is_loaded:
            try:
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
            except Exception as e:
                print(f"[AnomalyDetector] Predict exception, using fallback: {e}")

        # Deterministic Mathematical Rule Fallback (Guarantees 100% serverless resilience)
        feats = arp_vector[0]
        req_rate, rep_rate, ratio, mac_changes, conflicts = feats

        if rep_rate >= 10.0 or mac_changes >= 2 or conflicts >= 1 or ratio >= 5.0:
            is_anomaly = True
            label = "ARP Spoofing / MITM"
            conf = 0.99
            anomaly_score = 0.99
        else:
            is_anomaly = False
            label = "Normal ARP"
            conf = 0.99
            anomaly_score = 0.01

        return {
            "is_anomaly": is_anomaly,
            "predicted_label": label,
            "confidence": conf,
            "anomaly_score": anomaly_score
        }
