import numpy as np

class FeatureExtractor:
    """
    Extracts numerical feature vectors for the Flow Deep Learning Model
    and the Protocol ARP Anomaly Detector from raw traffic objects or dictionaries.
    """
    FLOW_FEATURES = [
        "flow_duration", "total_fwd_packets", "total_bwd_packets",
        "flow_bytes_s", "flow_packets_s", "fwd_pkt_len_mean",
        "bwd_pkt_len_mean", "syn_flag_count", "rst_flag_count",
        "ack_flag_count", "dst_port", "failed_auth_attempts"
    ]

    ARP_FEATURES = [
        "arp_request_rate", "arp_reply_rate", "arp_reply_req_ratio",
        "mac_change_rate", "ip_mac_binding_conflicts"
    ]

    @staticmethod
    def extract_flow_features(flow_dict):
        """Converts flow dictionary into scaled numpy vector for DL flow model."""
        vector = []
        for feature in FeatureExtractor.FLOW_FEATURES:
            vector.append(float(flow_dict.get(feature, 0.0)))
        return np.array([vector])

    @staticmethod
    def extract_arp_features(arp_dict):
        """Converts ARP metrics dictionary into numpy vector for anomaly model."""
        vector = []
        for feature in FeatureExtractor.ARP_FEATURES:
            vector.append(float(arp_dict.get(feature, 0.0)))
        return np.array([vector])
