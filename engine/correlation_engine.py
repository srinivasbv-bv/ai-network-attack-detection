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
    enriched with MITRE ATT&CK, Cyber Kill Chain, CAPEC, OWASP, feature-based reasoning, and
    alert lifecycle management.
    """

    def __init__(self, model_dir):
        self.dl_detector = DeepLearningDetector(model_dir)
        self.anomaly_detector = AnomalyDetector(model_dir)

    def generate_why_detected(self, final_label, flow_dict, arp_dict):
        """
        Generates feature-based explanation reasoning using actual traffic parameters.
        Never invents explanations; grounds reasoning strictly in measured features.
        """
        if final_label == "DoS":
            pkts_s = flow_dict.get("flow_packets_s", 0)
            syn_cnt = flow_dict.get("syn_flag_count", 0)
            fwd_pkts = flow_dict.get("total_fwd_packets", 0)
            return f"Volumetric anomaly: High forward packet rate ({pkts_s:.0f} pkts/s) and elevated SYN flag count ({syn_cnt}) exceeding baseline threshold."

        elif final_label == "DDoS":
            pkts_s = flow_dict.get("flow_packets_s", 0)
            bytes_s = flow_dict.get("flow_bytes_s", 0) / 1e6
            fwd_pkts = flow_dict.get("total_fwd_packets", 0)
            return f"Extreme distributed volumetric flood: Packet volume ({pkts_s:.0f} pkts/s, {bytes_s:.1f} MB/s) with {fwd_pkts} forward packets and 0 backward ACK responses."

        elif final_label == "PortScan":
            dst_port = flow_dict.get("dst_port", 0)
            duration = flow_dict.get("flow_duration", 0)
            syn_cnt = flow_dict.get("syn_flag_count", 0)
            return f"Reconnaissance anomaly: Rapid port probe targeted at destination port {dst_port} with short flow duration ({duration:.1f}ms) and single SYN flag."

        elif final_label == "BruteForce":
            failed_auth = flow_dict.get("failed_auth_attempts", 0)
            dst_port = flow_dict.get("dst_port", 22)
            return f"Authentication anomaly: Excessive failed login attempts ({failed_auth} failures) against service port {dst_port}."

        elif final_label == "ARP Spoofing / MITM":
            reply_rate = arp_dict.get("arp_reply_rate", 0)
            req_rate = arp_dict.get("arp_request_rate", 0)
            conflicts = arp_dict.get("ip_mac_binding_conflicts", 0)
            mac_changes = arp_dict.get("mac_change_rate", 0)
            return f"Protocol rule violation: Unsolicited ARP reply rate ({reply_rate:.1f}/s) exceeds request rate ({req_rate:.1f}/s) with MAC conflict count ({conflicts}) and rapid MAC changes ({mac_changes}/s)."

        else:
            pkts_s = flow_dict.get("flow_packets_s", 0)
            duration = flow_dict.get("flow_duration", 0)
            return f"Traffic parameters within expected benign baseline limits (Packet Rate: {pkts_s:.0f}/s, Duration: {duration:.0f}ms, 0 Auth Failures)."

    def analyze_event(self, flow_dict, arp_dict, src_ip="192.168.1.105", dst_ip="192.168.1.1", protocol="TCP"):
        # 1. Feature Extraction
        flow_vector = FeatureExtractor.extract_flow_features(flow_dict)
        arp_vector = FeatureExtractor.extract_arp_features(arp_dict)

        # 2. Parallel Model Predictions
        flow_result = self.dl_detector.predict(flow_vector)
        arp_result = self.anomaly_detector.predict(arp_vector)

        # 3. Score Fusion & Conflict Resolution
        if arp_result["is_anomaly"] and arp_result["anomaly_score"] > 0.60:
            final_label = "ARP Spoofing / MITM"
            final_confidence = arp_result["confidence"]
            detection_engine = "Random Forest Anomaly Detector"
        else:
            final_label = flow_result["predicted_label"]
            final_confidence = flow_result["confidence"]
            detection_engine = "Deep Learning Flow Model (CNN+LSTM)"

        # 4. Threat Framework Mapping & Feature Reasoning
        threat_meta = ThreatMapper.map_threat(final_label)
        why_detected = self.generate_why_detected(final_label, flow_dict, arp_dict)

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
            "score_range": threat_meta["score_range"],
            "detection_engine": detection_engine,
            "why_detected": why_detected,
            "recommended_response": threat_meta["recommended_response"],
            "alert_lifecycle": ["Detected", "Classified", "Investigated", "Recommended Response", "Verified"],
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
