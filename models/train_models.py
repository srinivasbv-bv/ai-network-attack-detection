import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure dataset generator can be called if datasets are missing
import sys
sys.path.append(BASE_DIR)
from data.dataset_generator import generate_flow_dataset, generate_arp_anomaly_dataset

def calculate_fpr(conf_matrix):
    """Calculates overall False Positive Rate from confusion matrix."""
    conf_matrix = np.array(conf_matrix)
    if conf_matrix.shape == (2, 2):
        tn, fp, fn, tp = conf_matrix.ravel()
        return float(fp / (fp + tn + 1e-7))
    else:
        # For multi-class, compute average FPR across classes
        fpr_list = []
        for i in range(len(conf_matrix)):
            fp = conf_matrix[:, i].sum() - conf_matrix[i, i]
            tn = conf_matrix.sum() - (conf_matrix[i, :].sum() + conf_matrix[:, i].sum() - conf_matrix[i, i])
            fpr = fp / (fp + tn + 1e-7)
            fpr_list.append(fpr)
        return float(np.mean(fpr_list))

def train():
    os.makedirs(MODELS_DIR, exist_ok=True)

    flow_path = os.path.join(DATA_DIR, "flow_dataset.csv")
    arp_path = os.path.join(DATA_DIR, "arp_anomaly_dataset.csv")

    if not os.path.exists(flow_path):
        generate_flow_dataset()
    if not os.path.exists(arp_path):
        generate_arp_anomaly_dataset()

    print("\n=======================================================")
    print(" 1. TRAINING DEEP LEARNING FLOW MODEL (LSTM/CNN/MLP)")
    print("=======================================================")
    df_flow = pd.read_csv(flow_path)
    X_flow = df_flow.drop(columns=["label"])
    y_flow = df_flow["label"]

    X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(
        X_flow, y_flow, test_size=0.2, random_state=42, stratify=y_flow
    )

    scaler_flow = StandardScaler()
    X_train_f_scaled = scaler_flow.fit_transform(X_train_f)
    X_test_f_scaled = scaler_flow.transform(X_test_f)

    # Deep Learning Flow Model (Multi-Layer Perceptron representing Deep Neural Net / Sequence Features)
    dl_flow_model = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        activation='relu',
        solver='adam',
        max_iter=300,
        random_state=42
    )
    dl_flow_model.fit(X_train_f_scaled, y_train_f)

    y_pred_f = dl_flow_model.predict(X_test_f_scaled)
    acc_f = accuracy_score(y_test_f, y_pred_f)
    prec_f, rec_f, f1_f, _ = precision_recall_fscore_support(y_test_f, y_pred_f, average='weighted')
    cm_f = confusion_matrix(y_test_f, y_pred_f).tolist()
    fpr_f = calculate_fpr(cm_f)

    print(f" Flow Model Accuracy  : {acc_f * 100:.2f}%")
    print(f" Flow Model Precision : {prec_f * 100:.2f}%")
    print(f" Flow Model Recall    : {rec_f * 100:.2f}%")
    print(f" Flow Model F1-Score  : {f1_f * 100:.2f}%")
    print(f" Flow Model FPR       : {fpr_f * 100:.2f}%")

    print("\n=======================================================")
    print(" 2. TRAINING ARP ANOMALY DETECTOR (RANDOM FOREST)")
    print("=======================================================")
    df_arp = pd.read_csv(arp_path)
    X_arp = df_arp.drop(columns=["label"])
    y_arp = df_arp["label"]

    X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(
        X_arp, y_arp, test_size=0.2, random_state=42, stratify=y_arp
    )

    scaler_arp = StandardScaler()
    X_train_a_scaled = scaler_arp.fit_transform(X_train_a)
    X_test_a_scaled = scaler_arp.transform(X_test_a)

    rf_arp_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_arp_model.fit(X_train_a_scaled, y_train_a)

    y_pred_a = rf_arp_model.predict(X_test_a_scaled)
    acc_a = accuracy_score(y_test_a, y_pred_a)
    prec_a, rec_a, f1_a, _ = precision_recall_fscore_support(y_test_a, y_pred_a, average='binary')
    cm_a = confusion_matrix(y_test_a, y_pred_a).tolist()
    fpr_a = calculate_fpr(cm_a)

    print(f" ARP Anomaly Accuracy : {acc_a * 100:.2f}%")
    print(f" ARP Anomaly Precision: {prec_a * 100:.2f}%")
    print(f" ARP Anomaly Recall   : {rec_a * 100:.2f}%")
    print(f" ARP Anomaly F1-Score : {f1_a * 100:.2f}%")
    print(f" ARP Anomaly FPR      : {fpr_a * 100:.2f}%")

    # Save artifacts
    joblib.dump(dl_flow_model, os.path.join(MODELS_DIR, "dl_flow_model.joblib"))
    joblib.dump(rf_arp_model, os.path.join(MODELS_DIR, "rf_arp_model.joblib"))
    joblib.dump(scaler_flow, os.path.join(MODELS_DIR, "flow_scaler.joblib"))
    joblib.dump(scaler_arp, os.path.join(MODELS_DIR, "arp_scaler.joblib"))

    metrics = {
        "flow_model": {
            "accuracy": float(acc_f),
            "precision": float(prec_f),
            "recall": float(rec_f),
            "f1_score": float(f1_f),
            "fpr": float(fpr_f),
            "confusion_matrix": cm_f,
            "classes": ["Normal", "DoS", "DDoS", "PortScan", "BruteForce"]
        },
        "arp_anomaly_model": {
            "accuracy": float(acc_a),
            "precision": float(prec_a),
            "recall": float(rec_a),
            "f1_score": float(f1_a),
            "fpr": float(fpr_a),
            "confusion_matrix": cm_a,
            "classes": ["Normal ARP", "ARP Spoofing / MITM"]
        }
    }

    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"\n[Model Trainer] Models and evaluation metrics successfully saved to {MODELS_DIR}")
    return metrics

if __name__ == "__main__":
    train()
