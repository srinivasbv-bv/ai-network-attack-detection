# AI-Powered Network Attack Detection System Using Deep Learning and Anomaly Detection

**Synopsis of MCA Project**  
*Submitted in partial fulfillment of the requirements for the award of the degree of Master of Science in Computer Science*  
**Karnataka State Open University (KSOU), Mysore**

---

## 📌 Project Overview

Network-based cyber-attacks such as Denial of Service (DoS), Distributed Denial of Service (DDoS), port scanning, brute-force login attempts, and Man-in-the-Middle (MITM)/ARP spoofing represent significant threats to modern infrastructure. Traditional signature-based Intrusion Detection Systems (IDS) fail against evolving and low-volume attack patterns.

This project delivers a complete **AI-Powered Network Attack Detection System** combining:
1. **Flow-Based Deep Learning Engine (LSTM/CNN)** for volumetric and sequential attacks (**DoS, DDoS, Port Scanning, Brute-Force**).
2. **Machine-Learning Anomaly Detector (Random Forest)** for protocol-level attacks (**MITM / ARP Spoofing**).
3. **Ensemble Correlation Engine**: Fuses dual-path probabilities and resolves signal conflicts into a single classified security alert.
4. **Threat Framework Mapping**: Maps every detection to **MITRE ATT&CK**, **Cyber Kill Chain**, **CAPEC**, and **OWASP Top 10**.
5. **ELK Stack Integration**: Normalizes events into Elastic Common Schema (ECS 8.x) JSON for Logstash/Elasticsearch ingestion and Kibana visualization.
6. **Real-time Live SOC Analyst Web Dashboard**: Modern dark glassmorphism interface featuring real-time SSE streaming, Chart.js analytics, MITRE heatmap grid, attack simulator, and ML evaluation metrics.

---

## 🛡️ Attack Category & Threat Framework Mapping

| Attack Category | MITRE ATT&CK Technique | Cyber Kill Chain Stage | CAPEC Reference | OWASP Top 10 Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Denial of Service (DoS)** | `T1499` – Endpoint Denial of Service | Actions on Objectives | CAPEC-125 (Flooding) | A05:2021 – Security Misconfiguration |
| **Distributed Denial of Service (DDoS)** | `T1498` – Network Denial of Service | Actions on Objectives | CAPEC-125 (Flooding) | A05:2021 – Resource Exhaustion |
| **Port Scanning** | `T1046` – Network Service Discovery | Reconnaissance | CAPEC-300 (Footprinting) | A05:2021 – Security Misconfiguration |
| **Brute-Force Attacks** | `T1110` – Brute Force | Credential Access | CAPEC-49 (Password Brute Forcing) | A07:2021 – Auth Failures |
| **MITM / ARP Spoofing** | `T1557` – Adversary-in-the-Middle | Credential Access / Collection | CAPEC-94 (Man-in-the-Middle) | A02:2021 – Cryptographic Failures |

---

## 📁 Directory Structure

```
ai_network_attack_detection/
├── data/                         # Flow & ARP anomaly benchmark dataset generators
│   └── dataset_generator.py
├── models/                       # Trained Deep Learning & ML model weights & metrics
│   ├── train_models.py
│   ├── dl_flow_model.joblib
│   ├── rf_arp_model.joblib
│   ├── flow_scaler.joblib
│   ├── arp_scaler.joblib
│   └── model_metrics.json
├── engine/                       # Core detection & threat mapping engine
│   ├── feature_extractor.py
│   ├── dl_detector.py
│   ├── anomaly_detector.py
│   ├── correlation_engine.py
│   └── threat_mapper.py
├── traffic/                      # Real-time traffic capture & attack stream simulator
│   └── traffic_simulator.py
├── elk/                          # Elastic Common Schema (ECS) exporter & Logstash pipeline
│   ├── elk_exporter.py
│   └── logstash.conf
├── web/                          # SOC Analyst Web Application
│   ├── app.py
│   ├── static/css/style.css
│   ├── static/js/dashboard.js
│   └── templates/index.html
├── docs/                         # Final Year Project Report & Defense Guide
│   └── PROJECT_REPORT.md
├── main.py                       # Single-command launcher
└── requirements.txt              # Dependencies
```

---

## 🚀 Quickstart & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the System
Execute the master single-entrypoint script:
```bash
python main.py
```
*Note: If datasets or trained models are missing, `main.py` will automatically generate the synthetic CICIDS2017/UNSW-NB15 flow data and train both models before starting the web server.*

### 3. Access SOC Analyst Web Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Model Performance & Evaluation Summary

| Model Component | Architecture | Accuracy | Precision | Recall | F1-Score | False Positive Rate (FPR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Flow Volumetric Engine** | Deep Learning (MLP/LSTM) | **99.85%** | **99.85%** | **99.85%** | **99.85%** | **0.04%** |
| **Protocol Anomaly Engine** | Random Forest | **100.00%** | **100.00%** | **100.00%** | **100.00%** | **0.00%** |

---

## 📊 ELK Stack (Elasticsearch, Logstash, Kibana) Integration

1. The system formats every detection into Elastic Common Schema (ECS 8.x) JSON.
2. Events are logged to `logs/network_security_events.json` and posted via HTTP to Logstash on port `5044`.
3. To start Logstash:
   ```bash
   logstash -f elk/logstash.conf
   ```
4. Detections are indexed into Elasticsearch under `network-security-events-*` and ready for visual analytics in Kibana.
