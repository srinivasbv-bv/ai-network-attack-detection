import os
import sys
import json
import time
from flask import Flask, render_template, Response, jsonify, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from engine.correlation_engine import EnsembleCorrelationEngine
from traffic.traffic_simulator import NetworkTrafficSimulator
from elk.elk_exporter import ELKExporter

template_dir = os.path.join(BASE_DIR, "web", "templates")
static_dir = os.path.join(BASE_DIR, "web", "static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

MODELS_DIR = os.path.join(BASE_DIR, "models")
engine = EnsembleCorrelationEngine(MODELS_DIR)
simulator = NetworkTrafficSimulator(engine)
exporter = ELKExporter()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stream")
def stream_traffic():
    def generate():
        max_iters = 5 if os.environ.get("VERCEL") else 300
        count = 0
        while count < max_iters:
            event = simulator.generate_next_event()
            exporter.export_event(event)

            data = {
                "event": event,
                "stats": simulator.get_stats()
            }
            yield f"data: {json.dumps(data)}\n\n"
            count += 1
            time.sleep(1.0)

    return Response(generate(), mimetype="text/event-stream")

@app.route("/api/next_event", methods=["GET"])
def next_event():
    event = simulator.generate_next_event()
    exporter.export_event(event)
    return jsonify({"event": event, "stats": simulator.get_stats()})

@app.route("/api/toggle_demo", methods=["POST"])
def toggle_demo():
    req_data = request.get_json() or {}
    enabled = req_data.get("enabled", True)
    status = simulator.set_demo_mode(enabled)
    return jsonify({"status": "success", "demo_mode": status, "system_status": simulator.get_stats()["system_status"]})

@app.route("/api/trigger_attack", methods=["POST"])
def trigger_attack():
    req_data = request.get_json() or {}
    attack_type = req_data.get("attack_type", "DoS")
    intensity = req_data.get("intensity", "Medium")
    simulator.set_manual_attack(attack_type, intensity=intensity)
    return jsonify({"status": "success", "message": f"Attack type '{attack_type}' ({intensity} intensity) injected into traffic stream."})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(simulator.get_stats())

@app.route("/api/recent_alerts", methods=["GET"])
def get_recent_alerts():
    alerts = simulator.get_recent_alerts(limit=25)
    return jsonify(alerts)

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "Model metrics not trained yet."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
