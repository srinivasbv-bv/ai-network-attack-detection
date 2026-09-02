class ThreatMapper:
    """
    Maps detected attack classifications to standard threat frameworks:
    - MITRE ATT&CK Technique ID & Title
    - Lockheed Martin Cyber Kill Chain Stage
    - CAPEC Reference (Common Attack Pattern Enumeration and Classification)
    - OWASP Top 10 Reference (where applicable)
    - Recommended Analyst Response Actions
    """

    MAPPING_TABLE = {
        "Normal": {
            "mitre_id": "N/A",
            "mitre_technique": "Benign Network Traffic",
            "kill_chain_stage": "Normal Operations",
            "capec": "N/A",
            "owasp": "N/A",
            "severity": "Low",
            "score_range": "0 - 29 (Low Risk)",
            "description": "Standard legitimate network communication adhering to baseline rules.",
            "recommended_response": "Recommended Analyst Action: No intervention required. Normal baseline traffic."
        },
        "DoS": {
            "mitre_id": "T1499",
            "mitre_technique": "Endpoint Denial of Service",
            "kill_chain_stage": "Actions on Objectives",
            "capec": "CAPEC-125 (Flooding)",
            "owasp": "A05:2021 - Security Misconfiguration / Resource Exhaustion",
            "severity": "High",
            "score_range": "60 - 84 (High Risk)",
            "description": "High-volume flooding traffic originating from a single source attempting to degrade or crash target endpoint.",
            "recommended_response": "Recommended Analyst Action: Apply source IP rate-limiting on border router and enforce ACL blocking rule for offender IP."
        },
        "DDoS": {
            "mitre_id": "T1498",
            "mitre_technique": "Network Denial of Service",
            "kill_chain_stage": "Actions on Objectives",
            "capec": "CAPEC-125 (Flooding)",
            "owasp": "A05:2021 - Security Misconfiguration / Resource Exhaustion",
            "severity": "Critical",
            "score_range": "85 - 100 (Critical Risk)",
            "description": "Coordinated multi-source high-volume traffic flooding network links and exhausting bandwidth.",
            "recommended_response": "Recommended Analyst Action: Enable edge DDoS scrubbing, rate-limit botnet subnet, and notify ISP upstream provider."
        },
        "PortScan": {
            "mitre_id": "T1046",
            "mitre_technique": "Network Service Discovery",
            "kill_chain_stage": "Reconnaissance",
            "capec": "CAPEC-300 (Footprinting)",
            "owasp": "A05:2021 - Security Misconfiguration",
            "severity": "Medium",
            "score_range": "30 - 59 (Medium Risk)",
            "description": "Reconnaissance scanning probing destination ports to identify open services and vulnerable software versions.",
            "recommended_response": "Recommended Analyst Action: Flag scanning source IP for monitoring, block probed unassigned destination ports, and verify firewall state."
        },
        "BruteForce": {
            "mitre_id": "T1110",
            "mitre_technique": "Brute Force",
            "kill_chain_stage": "Credential Access",
            "capec": "CAPEC-49 (Password Brute Forcing)",
            "owasp": "A07:2021 - Identification and Authentication Failures",
            "severity": "High",
            "score_range": "60 - 84 (High Risk)",
            "description": "Repeated systematic authentication attempts against SSH, FTP, or RDP services.",
            "recommended_response": "Recommended Analyst Action: Enforce temporary IP ban on targeted service, trigger mandatory credential reset, and enforce 2FA."
        },
        "ARP Spoofing / MITM": {
            "mitre_id": "T1557",
            "mitre_technique": "Adversary-in-the-Middle",
            "kill_chain_stage": "Credential Access / Collection",
            "capec": "CAPEC-94 (Man-in-the-Middle)",
            "owasp": "A02:2021 - Cryptographic Failures",
            "severity": "Critical",
            "score_range": "85 - 100 (Critical Risk)",
            "description": "Stateless ARP table poisoning altering IP-to-MAC bindings to intercept or modify local network traffic.",
            "recommended_response": "Recommended Analyst Action: Flush local ARP cache, enforce static IP-MAC bindings on gateway, and isolate switch port."
        }
    }

    @staticmethod
    def map_threat(attack_category):
        """Returns threat framework metadata for a given attack category string."""
        return ThreatMapper.MAPPING_TABLE.get(attack_category, ThreatMapper.MAPPING_TABLE["Normal"])
