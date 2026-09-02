import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

def check_and_prepare_environment():
    """Verifies that datasets and trained models are present before launching."""
    print("=========================================================================")
    print(" AI POWERED THREAT DETECTION SYSTEM")
    print(" MCA Final Year Project • Karnataka State Open University (KSOU)")
    print("=========================================================================\n")

    data_dir = os.path.join(BASE_DIR, "data")
    models_dir = os.path.join(BASE_DIR, "models")
    flow_data = os.path.join(data_dir, "flow_dataset.csv")
    dl_model = os.path.join(models_dir, "dl_flow_model.joblib")

    if not os.path.exists(flow_data) or not os.path.exists(dl_model):
        print("[System Launcher] Datasets or trained models missing. Initializing training pipeline...")
        from models.train_models import train
        train()
    else:
        print("[System Launcher] Trained ML/DL models & feature datasets verified.")

def launch_web_app():
    print("\n[System Launcher] Launching SOC Analyst Web Dashboard on http://127.0.0.1:5000 ...")
    from web.app import app
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    check_and_prepare_environment()
    launch_web_app()
