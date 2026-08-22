import uuid
import datetime
from .feature_extractor import FeatureExtractor
from .dl_detector import DeepLearningDetector
from .anomaly_detector import AnomalyDetector
from .threat_mapper import ThreatMapper

class EnsembleCorrelationEngine:
    """
    Fuses outputs from the Deep Learning flow classifier and the Machine Learning protocol
    anomaly detector. Resolves conflicting signals and produces a single unified security event
    enriched with MITRE ATT&CK, Cyber Kill Chain, CAPEC, and OWASP framework context.
    """

    def __init__(self, model_dir):
        self.dl_detector = DeepLearningDetector(model_dir)
        self.anomaly_detector = AnomalyDetector(model_dir)

    def analyze_event(self, flow_dict, arp_dict, src_ip="192.168.1.105", dst_ip="192.168.1.1", protocol="TCP"):
        # 1. Feature Extraction
        flow_vector = FeatureExtractor.extract_flow_features(flow_dict)
        arp_vector = FeatureExtractor.extract_arp_features(arp_dict)

        # 2. Parallel Model Predictions
        flow_result = self.dl_detector.predict(flow_vector)
        arp_result = self.anomaly_detector.predict(arp_vector)

        # 3. Score Fusion & Conflict Resolution
        # If protocol anomaly score exceeds threshold (> 0.65), prioritize ARP Spoofing / MITM detection
        if arp_result["is_anomaly"] and arp_result["anomaly_score"] > 0.60:
            final_label = "ARP Spoofing / MITM"
            final_confidence = arp_result["confidence"]
            detection_engine = "Random Forest Anomaly Detector"
        else:
            final_label = flow_result["predicted_label"]
            final_confidence = flow_result["confidence"]
            detection_engine = "Deep Learning Flow Model (LSTM/CNN)"

        # 4. Threat Framework Mapping
        threat_meta = ThreatMapper.map_threat(final_label)

        # Calculate overall Threat Score (0 - 100)
        base_scores = {"Normal": 5, "PortScan": 45, "BruteForce": 75, "DoS": 85, "DDoS": 98, "ARP Spoofing / MITM": 95}
        raw_score = base_scores.get(final_label, 10)
        threat_score = round(raw_score * final_confidence, 1)

        event_id = f"ALERT-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        # 5. Formulate Standard Security Event Payload
        event_payload = {
            "event_id": event_id,
            "timestamp": timestamp,
            "source_ip": src_ip,
            "destination_ip": dst_ip,
            "protocol": protocol,
            "classification": final_label,
            "confidence": round(final_confidence * 100, 1),
            "threat_score": threat_score,
            "severity": threat_meta["severity"],
            "detection_engine": detection_engine,
            "mitre_id": threat_meta["mitre_id"],
            "mitre_technique": threat_meta["mitre_technique"],
            "kill_chain_stage": threat_meta["kill_chain_stage"],
            "capec_reference": threat_meta["capec"],
            "owasp_reference": threat_meta["owasp"],
            "description": threat_meta["description"],
            "raw_features": {
                "flow": flow_dict,
                "protocol": arp_dict
            },
            "model_breakdown": {
                "dl_flow_prediction": flow_result,
                "rf_arp_prediction": arp_result
            }
        }

        return event_payload
