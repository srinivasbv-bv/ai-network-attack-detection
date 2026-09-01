import os
import json
import requests

class ELKExporter:
    """
    Elastic Common Schema (ECS) Exporter.
    Formats detection events into ECS-compliant JSON payloads and forwards them to
    Logstash or Elasticsearch REST APIs, while keeping a local indexed log file.
    """

    def __init__(self, logstash_url="http://localhost:5044", elasticsearch_url="http://localhost:9200", log_dir=None):
        self.logstash_url = logstash_url
        self.elasticsearch_url = elasticsearch_url

        if log_dir is None:
            try:
                log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
                os.makedirs(log_dir, exist_ok=True)
            except Exception:
                log_dir = "/tmp"

        try:
            self.local_log_file = os.path.join(log_dir, "network_security_events.json")
        except Exception:
            self.local_log_file = None

    def format_ecs(self, alert_event):
        """Converts internal security event to Elastic Common Schema (ECS 8.x format)."""
        ecs_payload = {
            "@timestamp": alert_event.get("timestamp"),
            "event": {
                "id": alert_event.get("event_id"),
                "kind": "alert",
                "category": ["network", "intrusion_detection"],
                "type": ["info"] if alert_event.get("classification") == "Normal" else ["denial_of_service", "indicator"],
                "outcome": "success" if alert_event.get("classification") == "Normal" else "failure",
                "severity": alert_event.get("threat_score"),
                "dataset": "ai_ids.network_threats"
            },
            "source": {
                "ip": alert_event.get("source_ip")
            },
            "destination": {
                "ip": alert_event.get("destination_ip")
            },
            "network": {
                "transport": alert_event.get("protocol"),
                "application": alert_event.get("classification")
            },
            "threat": {
                "framework": "MITRE ATT&CK",
                "technique": {
                    "id": alert_event.get("mitre_id"),
                    "name": alert_event.get("mitre_technique")
                },
                "tactic": {
                    "name": alert_event.get("kill_chain_stage")
                },
                "enrichment": {
                    "capec": alert_event.get("capec_reference"),
                    "owasp": alert_event.get("owasp_reference"),
                    "detection_engine": alert_event.get("detection_engine"),
                    "confidence_pct": alert_event.get("confidence")
                }
            },
            "message": f"[{alert_event.get('severity')}] {alert_event.get('classification')} detected from {alert_event.get('source_ip')} -> {alert_event.get('destination_ip')}"
        }
        return ecs_payload

    def export_event(self, alert_event):
        ecs_event = self.format_ecs(alert_event)

        # 1. Write to local JSON log file (line-delimited JSON)
        try:
            with open(self.local_log_file, "a") as f:
                f.write(json.dumps(ecs_event) + "\n")
        except Exception as e:
            print(f"[ELK Exporter File Error] {e}")

        # 2. Attempt forward to HTTP Logstash / Elasticsearch endpoint (Non-blocking retry)
        try:
            headers = {"Content-Type": "application/json"}
            requests.post(self.logstash_url, json=ecs_event, headers=headers, timeout=0.5)
        except Exception:
            # Silent fallback if local ELK stack is not running
            pass

        return ecs_event
