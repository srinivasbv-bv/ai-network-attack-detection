import time
import random
import threading
from collections import deque

class NetworkTrafficSimulator:
    """
    Simulates live network packet flows and protocol metrics.
    Can run in continuous background mode or execute user-triggered attack vectors.
    """

    def __init__(self, correlation_engine, max_history=100):
        self.engine = correlation_engine
        self.max_history = max_history
        self.alert_history = deque(maxlen=max_history)
        self.is_running = False
        self.lock = threading.Lock()
        self.active_manual_attack = None
        self.stats = {
            "total_events": 0,
            "normal_count": 0,
            "attack_count": 0,
            "dos_count": 0,
            "ddos_count": 0,
            "portscan_count": 0,
            "bruteforce_count": 0,
            "mitm_count": 0,
            "latest_threat_score": 0
        }

    def set_manual_attack(self, attack_type):
        """Injects a specific attack type into the live traffic stream."""
        self.active_manual_attack = attack_type

    def generate_simulated_traffic(self, attack_type=None):
        """Generates synthetic flow & protocol metrics matching a chosen traffic type."""
        if attack_type is None:
            # 85% Normal traffic, 15% random background attacks
            attack_type = random.choices(
                ["Normal", "DoS", "DDoS", "PortScan", "BruteForce", "ARP Spoofing / MITM"],
                weights=[0.85, 0.03, 0.03, 0.03, 0.03, 0.03]
            )[0]

        src_ips = ["192.168.1.102", "192.168.1.105", "10.0.0.45", "172.16.0.12", "192.168.1.210"]
        dst_ips = ["192.168.1.1", "192.168.1.10", "10.0.0.1", "172.16.0.1"]

        src_ip = random.choice(src_ips)
        dst_ip = random.choice(dst_ips)
        protocol = "TCP"

        if attack_type == "Normal":
            flow = {
                "flow_duration": random.uniform(20, 3000),
                "total_fwd_packets": random.randint(2, 30),
                "total_bwd_packets": random.randint(2, 40),
                "flow_bytes_s": random.uniform(1000, 40000),
                "flow_packets_s": random.uniform(2, 50),
                "fwd_pkt_len_mean": random.uniform(64, 1400),
                "bwd_pkt_len_mean": random.uniform(64, 1400),
                "syn_flag_count": random.choice([0, 1]),
                "rst_flag_count": 0,
                "ack_flag_count": random.randint(1, 50),
                "dst_port": random.choice([80, 443, 53, 8080]),
                "failed_auth_attempts": 0
            }
            arp = {
                "arp_request_rate": random.uniform(0.1, 2.0),
                "arp_reply_rate": random.uniform(0.1, 2.0),
                "arp_reply_req_ratio": 1.0,
                "mac_change_rate": 0,
                "ip_mac_binding_conflicts": 0
            }

        elif attack_type == "DoS":
            flow = {
                "flow_duration": random.uniform(500, 2000),
                "total_fwd_packets": random.randint(800, 4000),
                "total_bwd_packets": random.randint(0, 5),
                "flow_bytes_s": random.uniform(800000, 4000000),
                "flow_packets_s": random.uniform(1000, 5000),
                "fwd_pkt_len_mean": random.uniform(128, 512),
                "bwd_pkt_len_mean": 0,
                "syn_flag_count": random.randint(500, 2000),
                "rst_flag_count": random.randint(100, 400),
                "ack_flag_count": 0,
                "dst_port": 80,
                "failed_auth_attempts": 0
            }
            arp = {"arp_request_rate": 1.0, "arp_reply_rate": 1.0, "arp_reply_req_ratio": 1.0, "mac_change_rate": 0, "ip_mac_binding_conflicts": 0}

        elif attack_type == "DDoS":
            src_ip = f"172.24.{random.randint(1, 254)}.{random.randint(1, 254)}" # Botnet IP
            flow = {
                "flow_duration": random.uniform(100, 800),
                "total_fwd_packets": random.randint(5000, 15000),
                "total_bwd_packets": 0,
                "flow_bytes_s": random.uniform(5000000, 18000000),
                "flow_packets_s": random.uniform(8000, 25000),
                "fwd_pkt_len_mean": random.uniform(64, 256),
                "bwd_pkt_len_mean": 0,
                "syn_flag_count": random.randint(2000, 8000),
                "rst_flag_count": random.randint(500, 1200),
                "ack_flag_count": 0,
                "dst_port": random.choice([80, 443]),
                "failed_auth_attempts": 0
            }
            arp = {"arp_request_rate": 1.0, "arp_reply_rate": 1.0, "arp_reply_req_ratio": 1.0, "mac_change_rate": 0, "ip_mac_binding_conflicts": 0}

        elif attack_type == "PortScan":
            flow = {
                "flow_duration": random.uniform(2, 50),
                "total_fwd_packets": random.randint(1, 3),
                "total_bwd_packets": 0,
                "flow_bytes_s": random.uniform(100, 1500),
                "flow_packets_s": random.uniform(50, 500),
                "fwd_pkt_len_mean": random.uniform(40, 64),
                "bwd_pkt_len_mean": 0,
                "syn_flag_count": 1,
                "rst_flag_count": 1,
                "ack_flag_count": 0,
                "dst_port": random.randint(1, 65535),
                "failed_auth_attempts": 0
            }
            arp = {"arp_request_rate": 1.0, "arp_reply_rate": 1.0, "arp_reply_req_ratio": 1.0, "mac_change_rate": 0, "ip_mac_binding_conflicts": 0}

        elif attack_type == "BruteForce":
            flow = {
                "flow_duration": random.uniform(3000, 12000),
                "total_fwd_packets": random.randint(100, 300),
                "total_bwd_packets": random.randint(80, 250),
                "flow_bytes_s": random.uniform(10000, 60000),
                "flow_packets_s": random.uniform(10, 40),
                "fwd_pkt_len_mean": random.uniform(150, 350),
                "bwd_pkt_len_mean": random.uniform(150, 350),
                "syn_flag_count": random.randint(10, 30),
                "rst_flag_count": random.randint(5, 20),
                "ack_flag_count": random.randint(100, 250),
                "dst_port": random.choice([22, 21, 3389]),
                "failed_auth_attempts": random.randint(25, 120)
            }
            arp = {"arp_request_rate": 1.0, "arp_reply_rate": 1.0, "arp_reply_req_ratio": 1.0, "mac_change_rate": 0, "ip_mac_binding_conflicts": 0}

        elif attack_type in ["ARP Spoofing / MITM", "MITM"]:
            protocol = "ARP"
            flow = {
                "flow_duration": random.uniform(500, 2000),
                "total_fwd_packets": random.randint(10, 50),
                "total_bwd_packets": random.randint(10, 50),
                "flow_bytes_s": random.uniform(2000, 15000),
                "flow_packets_s": random.uniform(5, 20),
                "fwd_pkt_len_mean": random.uniform(42, 60),
                "bwd_pkt_len_mean": random.uniform(42, 60),
                "syn_flag_count": 0,
                "rst_flag_count": 0,
                "ack_flag_count": 0,
                "dst_port": 0,
                "failed_auth_attempts": 0
            }
            arp = {
                "arp_request_rate": random.uniform(0.2, 2.0),
                "arp_reply_rate": random.uniform(25.0, 120.0), # High unsolicited reply flooding
                "arp_reply_req_ratio": random.uniform(15.0, 60.0),
                "mac_change_rate": random.randint(5, 20),       # MAC address rapid flipping
                "ip_mac_binding_conflicts": random.randint(2, 8)
            }

        # Analyze event through ensemble correlation engine
        event = self.engine.analyze_event(flow, arp, src_ip=src_ip, dst_ip=dst_ip, protocol=protocol)

        with self.lock:
            self.alert_history.appendleft(event)
            self.stats["total_events"] += 1
            if event["classification"] == "Normal":
                self.stats["normal_count"] += 1
            else:
                self.stats["attack_count"] += 1

            if event["classification"] == "DoS":
                self.stats["dos_count"] += 1
            elif event["classification"] == "DDoS":
                self.stats["ddos_count"] += 1
            elif event["classification"] == "PortScan":
                self.stats["portscan_count"] += 1
            elif event["classification"] == "BruteForce":
                self.stats["bruteforce_count"] += 1
            elif event["classification"] == "ARP Spoofing / MITM":
                self.stats["mitm_count"] += 1

            self.stats["latest_threat_score"] = event["threat_score"]

        return event

    def generate_next_event(self):
        """Generates the next event taking into account any active manual injection."""
        attack_type = self.active_manual_attack
        self.active_manual_attack = None # Reset manual trigger after 1 fire
        return self.generate_simulated_traffic(attack_type=attack_type)

    def get_recent_alerts(self, limit=20):
        with self.lock:
            return list(self.alert_history)[:limit]

    def get_stats(self):
        with self.lock:
            return dict(self.stats)
