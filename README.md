# AI POWERED THREAT DETECTION SYSTEM

**Final Year MCA Project Implementation**  
*Submitted in partial fulfillment of the requirements for the award of the degree of Master of Science in Computer Science*  
**Karnataka State Open University (KSOU), Mysore**

---

## 📌 Project Overview

Network-based cyber-attacks such as Denial of Service (DoS), Distributed Denial of Service (DDoS), port scanning, brute-force login attempts, and Man-in-the-Middle (MITM)/ARP spoofing represent significant threats to modern enterprise infrastructure. Traditional signature-based Intrusion Detection Systems (IDS) fail against evolving, obfuscated, and low-volume attack patterns.

This project delivers a complete, production-ready **AI POWERED THREAT DETECTION SYSTEM** combining:
1. **Flow-Based Deep Learning Engine (Deep Multi-Layer Perceptron / Deep MLP)** for volumetric and sequential attacks (**DoS, DDoS, Port Scanning, Brute-Force**).
2. **Machine-Learning Protocol Anomaly Detector (Random Forest)** for protocol-level attacks (**MITM / ARP Spoofing**).
3. **Ensemble Correlation Engine**: Fuses dual-path probabilities and resolves signal conflicts into a single classified security event enriched with feature-based reasoning explanations ("Why Was This Detected?").
4. **Threat Framework Mapping**: Maps every detection to **MITRE ATT&CK** (`T1499`, `T1498`, `T1046`, `T1110`, `T1557`), **Cyber Kill Chain**, **CAPEC**, and **OWASP Top 10**.
5. **ELK Stack Integration**: Normalizes events into Elastic Common Schema (ECS 8.x) JSON for Logstash/Elasticsearch ingestion and Kibana visualization.
6. **Real-time Live SOC Analyst Web Dashboard**: Features Demo Mode toggle, Live AI Prediction Card, Attack Intensity Simulator, MITRE Heatmap Matrix, Incident Investigation Drawer with 5-stage Alert Lifecycle (`Detected` ➔ `Classified` ➔ `Investigated` ➔ `Recommended Response` ➔ `Verified`), Confusion Matrix viewer, and System Limitations review.

---

## 🛡️ Attack Category & Threat Framework Mapping

| Attack Category | MITRE ATT&CK Technique | Cyber Kill Chain Stage | CAPEC Reference | OWASP Top 10 Reference | Risk Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Denial of Service (DoS)** | `T1499` – Endpoint Denial of Service | Actions on Objectives | CAPEC-125 (Flooding) | A05:2021 – Security Misconfiguration | **High** (60 - 84) |
| **Distributed Denial of Service (DDoS)** | `T1498` – Network Denial of Service | Actions on Objectives | CAPEC-125 (Flooding) | A05:2021 – Resource Exhaustion | **Critical** (85 - 100) |
| **Port Scanning** | `T1046` – Network Service Discovery | Reconnaissance | CAPEC-300 (Footprinting) | A05:2021 – Security Misconfiguration | **Medium** (30 - 59) |
| **Brute-Force Attacks** | `T1110` – Brute Force | Credential Access | CAPEC-49 (Password Brute Forcing) | A07:2021 – Auth Failures | **High** (60 - 84) |
| **MITM / ARP Spoofing** | `T1557` – Adversary-in-the-Middle | Credential Access / Collection | CAPEC-94 (Man-in-the-Middle) | A02:2021 – Cryptographic Failures | **Critical** (85 - 100) |

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
├── docs/                         # Documentation, Report & PDF Guide
│   ├── PROJECT_REPORT.md
│   └── AI_Network_Attack_Detection_Beginners_Guide.pdf
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
*Note: `main.py` automatically verifies model weights and initializes dataset generation if needed, then starts the Flask web server.*

### 3. Access SOC Analyst Web Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Model Performance & Evaluation Summary

| Model Component | Architecture | Accuracy | Precision | Recall | F1-Score | FPR | FNR |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Flow Volumetric Engine** | Deep Neural Network (Deep MLP) | **99.75%** | **99.75%** | **99.75%** | **99.75%** | **0.06%** | **0.25%** |
| **Protocol Anomaly Engine** | Random Forest (100 Trees) | **100.00%** | **100.00%** | **100.00%** | **100.00%** | **0.00%** | **0.00%** |

- **Dataset Info**: CICIDS2017 & UNSW-NB15 Flow Schema + ARP Anomaly Benchmark (14,000 total samples, 80/20 train/test split).

---

## 📊 ELK Stack (Elasticsearch, Logstash, Kibana) Integration

1. The system formats every detection into Elastic Common Schema (ECS 8.x) JSON.
2. Events are logged to `logs/network_security_events.json` and posted via HTTP to Logstash on port `5044`.
3. To start Logstash:
   ```bash
   logstash -f elk/logstash.conf
   ```
4. Detections are indexed into Elasticsearch under `network-security-events-*` and ready for visual analytics in Kibana.
