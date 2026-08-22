import os
import numpy as np
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_flow_dataset(num_samples=10000, random_seed=42):
    """
    Generates a realistic flow-based dataset replicating key feature distributions
    from benchmark intrusion detection datasets (CICIDS2017 / UNSW-NB15).
    Classes:
      0: Normal (Benign traffic)
      1: DoS (Denial of Service - single source flood)
      2: DDoS (Distributed DoS - coordinated high volume flood)
      3: PortScan (Reconnaissance port probes)
      4: BruteForce (Credential attacks on SSH/FTP/RDP)
    """
    np.random.seed(random_seed)
    samples_per_class = num_samples // 5

    data = []

    # 1. Normal Traffic
    for _ in range(samples_per_class):
        duration = np.random.uniform(10, 5000)
        fwd_pkts = np.random.randint(2, 50)
        bwd_pkts = np.random.randint(2, 60)
        bytes_s = np.random.uniform(500, 50000)
        pkts_s = (fwd_pkts + bwd_pkts) / (duration / 1000.0)
        fwd_len = np.random.uniform(40, 1500)
        bwd_len = np.random.uniform(40, 1500)
        syn_cnt = np.random.choice([0, 1], p=[0.7, 0.3])
        rst_cnt = np.random.choice([0, 1], p=[0.95, 0.05])
        ack_cnt = np.random.randint(1, 100)
        dst_port = np.random.choice([80, 443, 53, 8080, 22, 21])
        failed_auth = 0
        data.append([duration, fwd_pkts, bwd_pkts, bytes_s, pkts_s, fwd_len, bwd_len, syn_cnt, rst_cnt, ack_cnt, dst_port, failed_auth, 0])

    # 2. DoS Attack Traffic (Single source flood, high rate, high SYN/RST)
    for _ in range(samples_per_class):
        duration = np.random.uniform(100, 2000)
        fwd_pkts = np.random.randint(500, 5000)
        bwd_pkts = np.random.randint(0, 10)
        bytes_s = np.random.uniform(500000, 5000000)
        pkts_s = (fwd_pkts + bwd_pkts) / (duration / 1000.0)
        fwd_len = np.random.uniform(64, 512)
        bwd_len = np.random.uniform(0, 64)
        syn_cnt = np.random.randint(200, 2000)
        rst_cnt = np.random.randint(50, 500)
        ack_cnt = np.random.randint(0, 20)
        dst_port = np.random.choice([80, 443])
        failed_auth = 0
        data.append([duration, fwd_pkts, bwd_pkts, bytes_s, pkts_s, fwd_len, bwd_len, syn_cnt, rst_cnt, ack_cnt, dst_port, failed_auth, 1])

    # 3. DDoS Attack Traffic (Distributed multi-source flood, extreme packets/sec)
    for _ in range(samples_per_class):
        duration = np.random.uniform(50, 1000)
        fwd_pkts = np.random.randint(2000, 15000)
        bwd_pkts = np.random.randint(0, 5)
        bytes_s = np.random.uniform(2000000, 20000000)
        pkts_s = (fwd_pkts + bwd_pkts) / (duration / 1000.0)
        fwd_len = np.random.uniform(40, 256)
        bwd_len = np.random.uniform(0, 40)
        syn_cnt = np.random.randint(1000, 8000)
        rst_cnt = np.random.randint(200, 1500)
        ack_cnt = np.random.randint(0, 10)
        dst_port = np.random.choice([80, 443, 8080])
        failed_auth = 0
        data.append([duration, fwd_pkts, bwd_pkts, bytes_s, pkts_s, fwd_len, bwd_len, syn_cnt, rst_cnt, ack_cnt, dst_port, failed_auth, 2])

    # 4. PortScan Traffic (Rapid probing across multiple port numbers)
    for _ in range(samples_per_class):
        duration = np.random.uniform(1, 100)
        fwd_pkts = np.random.randint(1, 4)
        bwd_pkts = np.random.randint(0, 2)
        bytes_s = np.random.uniform(100, 2000)
        pkts_s = (fwd_pkts + bwd_pkts) / (duration / 1000.0)
        fwd_len = np.random.uniform(40, 80)
        bwd_len = np.random.uniform(0, 64)
        syn_cnt = 1
        rst_cnt = np.random.choice([0, 1], p=[0.4, 0.6])
        ack_cnt = 0
        dst_port = np.random.randint(1, 65535)
        failed_auth = 0
        data.append([duration, fwd_pkts, bwd_pkts, bytes_s, pkts_s, fwd_len, bwd_len, syn_cnt, rst_cnt, ack_cnt, dst_port, failed_auth, 3])

    # 5. BruteForce Attack Traffic (High authentication failure attempts)
    for _ in range(samples_per_class):
        duration = np.random.uniform(2000, 15000)
        fwd_pkts = np.random.randint(50, 300)
        bwd_pkts = np.random.randint(40, 250)
        bytes_s = np.random.uniform(5000, 50000)
        pkts_s = (fwd_pkts + bwd_pkts) / (duration / 1000.0)
        fwd_len = np.random.uniform(100, 400)
        bwd_len = np.random.uniform(100, 400)
        syn_cnt = np.random.randint(10, 50)
        rst_cnt = np.random.randint(5, 30)
        ack_cnt = np.random.randint(50, 300)
        dst_port = np.random.choice([22, 21, 3389]) # SSH, FTP, RDP
        failed_auth = np.random.randint(15, 150)
        data.append([duration, fwd_pkts, bwd_pkts, bytes_s, pkts_s, fwd_len, bwd_len, syn_cnt, rst_cnt, ack_cnt, dst_port, failed_auth, 4])

    columns = [
        "flow_duration", "total_fwd_packets", "total_bwd_packets",
        "flow_bytes_s", "flow_packets_s", "fwd_pkt_len_mean",
        "bwd_pkt_len_mean", "syn_flag_count", "rst_flag_count",
        "ack_flag_count", "dst_port", "failed_auth_attempts", "label"
    ]

    df = pd.DataFrame(data, columns=columns)
    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

    csv_path = os.path.join(DATA_DIR, "flow_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"[Dataset Generator] Flow dataset created: {csv_path} ({len(df)} samples)")
    return csv_path


def generate_arp_anomaly_dataset(num_samples=4000, random_seed=42):
    """
    Generates dataset for protocol-level MITM / ARP Spoofing anomaly detection.
    Features:
      - arp_request_rate: ARP requests per second
      - arp_reply_rate: ARP replies per second
      - arp_reply_req_ratio: Ratio of unrequested replies
      - mac_change_rate: Rapid MAC binding changes for a single IP address
      - ip_mac_binding_conflicts: Conflicting MAC entries in ARP table
      - label: 0 (Normal ARP traffic), 1 (ARP Spoofing / MITM Anomaly)
    """
    np.random.seed(random_seed)
    samples_half = num_samples // 2
    data = []

    # Normal ARP Behavior
    for _ in range(samples_half):
        req_rate = np.random.uniform(0.1, 3.0)
        rep_rate = np.random.uniform(0.1, 3.2)
        ratio = rep_rate / (req_rate + 1e-5)
        mac_changes = np.random.choice([0, 1], p=[0.95, 0.05])
        conflicts = 0
        data.append([req_rate, rep_rate, ratio, mac_changes, conflicts, 0])

    # ARP Spoofing / MITM Anomaly Behavior (Excessive unsolicited replies, high MAC change rate)
    for _ in range(samples_half):
        req_rate = np.random.uniform(0.2, 5.0)
        rep_rate = np.random.uniform(15.0, 150.0) # Gratuitous / unsolicited ARP replies
        ratio = rep_rate / (req_rate + 1e-5)
        mac_changes = np.random.randint(3, 25)    # High frequency MAC flipping
        conflicts = np.random.randint(1, 10)       # Conflicting IP-MAC bindings
        data.append([req_rate, rep_rate, ratio, mac_changes, conflicts, 1])

    columns = [
        "arp_request_rate", "arp_reply_rate", "arp_reply_req_ratio",
        "mac_change_rate", "ip_mac_binding_conflicts", "label"
    ]

    df = pd.DataFrame(data, columns=columns)
    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

    csv_path = os.path.join(DATA_DIR, "arp_anomaly_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"[Dataset Generator] ARP Anomaly dataset created: {csv_path} ({len(df)} samples)")
    return csv_path

if __name__ == "__main__":
    generate_flow_dataset()
    generate_arp_anomaly_dataset()
