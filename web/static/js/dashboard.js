let eventSource = null;
let isPaused = false;
let alertDataStore = [];

// Chart instances
let timelineChart = null;
let distributionChart = null;

const attackCategoryCounts = {
    "Normal": 0,
    "DoS": 0,
    "DDoS": 0,
    "PortScan": 0,
    "BruteForce": 0,
    "ARP Spoofing / MITM": 0
};

document.addEventListener("DOMContentLoaded", () => {
    initCharts();
    initSSE();
    fetchModelMetrics();

    document.getElementById("pauseStreamBtn").addEventListener("click", toggleStream);
    document.getElementById("alertSearch").addEventListener("input", filterAlerts);
});

function initCharts() {
    // Timeline Chart
    const ctxTimeline = document.getElementById("timelineChart").getContext("2d");
    timelineChart = new Chart(ctxTimeline, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Threat Index",
                data: [],
                borderColor: "#00f2fe",
                backgroundColor: "rgba(0, 242, 254, 0.1)",
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { display: false },
                y: { min: 0, max: 100, grid: { color: "rgba(255, 255, 255, 0.05)" } }
            },
            plugins: { legend: { display: false } }
        }
    });

    // Distribution Chart
    const ctxDist = document.getElementById("distributionChart").getContext("2d");
    distributionChart = new Chart(ctxDist, {
        type: "doughnut",
        data: {
            labels: ["Normal", "DoS", "DDoS", "PortScan", "BruteForce", "ARP/MITM"],
            datasets: [{
                data: [0, 0, 0, 0, 0, 0],
                backgroundColor: [
                    "#00e676", "#ff9100", "#ff3b5c", "#00e5ff", "#7928ca", "#e91e63"
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "right", labels: { color: "#8a99b5", font: { size: 11 } } }
            }
        }
    });
}

function initSSE() {
    eventSource = new EventSource("/api/stream");

    eventSource.onmessage = (e) => {
        if (isPaused) return;

        const payload = JSON.parse(e.data);
        const event = payload.event;
        const stats = payload.stats;

        updateStats(stats);
        addAlertToTable(event);
        updateCharts(event, stats);
        updateMitreMatrix(event);
    };

    eventSource.onerror = () => {
        console.warn("SSE connection interrupted. Reconnecting...");
    };
}

function toggleStream() {
    isPaused = !isPaused;
    const btn = document.getElementById("pauseStreamBtn");
    if (isPaused) {
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Resume Stream';
        btn.classList.add("btn-paused");
    } else {
        btn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause Stream';
        btn.classList.remove("btn-paused");
    }
}

function triggerAttack(attackType) {
    fetch("/api/trigger_attack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attack_type: attackType })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Attack injected:", data.message);
    })
    .catch(err => console.error("Error triggering attack:", err));
}

function updateStats(stats) {
    document.getElementById("statTotalEvents").innerText = stats.total_events.toLocaleString();
    document.getElementById("statNormalCount").innerText = stats.normal_count.toLocaleString();
    document.getElementById("statAttackCount").innerText = stats.attack_count.toLocaleString();
    document.getElementById("statThreatScore").innerText = stats.latest_threat_score;

    attackCategoryCounts["Normal"] = stats.normal_count;
    attackCategoryCounts["DoS"] = stats.dos_count;
    attackCategoryCounts["DDoS"] = stats.ddos_count;
    attackCategoryCounts["PortScan"] = stats.portscan_count;
    attackCategoryCounts["BruteForce"] = stats.bruteforce_count;
    attackCategoryCounts["ARP Spoofing / MITM"] = stats.mitm_count;

    document.getElementById("count-PortScan").innerText = `${stats.portscan_count} Intercepted`;
    document.getElementById("count-BruteForce").innerText = `${stats.bruteforce_count} Intercepted`;
    document.getElementById("count-MITM").innerText = `${stats.mitm_count} Intercepted`;
    document.getElementById("count-DoS").innerText = `${stats.dos_count} Intercepted`;
    document.getElementById("count-DDoS").innerText = `${stats.ddos_count} Intercepted`;
}

function updateCharts(event, stats) {
    // 1. Update Timeline
    const timestampLabel = event.timestamp.split("T")[1].substring(0, 8);
    timelineChart.data.labels.push(timestampLabel);
    timelineChart.data.datasets[0].data.push(event.threat_score);

    if (timelineChart.data.labels.length > 20) {
        timelineChart.data.labels.shift();
        timelineChart.data.datasets[0].data.shift();
    }
    timelineChart.update();

    // 2. Update Doughnut Distribution
    distributionChart.data.datasets[0].data = [
        stats.normal_count,
        stats.dos_count,
        stats.ddos_count,
        stats.portscan_count,
        stats.bruteforce_count,
        stats.mitm_count
    ];
    distributionChart.update();
}

function updateMitreMatrix(event) {
    const mitreId = event.mitre_id;
    if (mitreId && mitreId !== "N/A") {
        const card = document.getElementById(`mitre-${mitreId}`);
        if (card) {
            card.classList.add("active-threat");
            setTimeout(() => {
                card.classList.remove("active-threat");
            }, 1800);
        }
    }
}

function addAlertToTable(event) {
    alertDataStore.unshift(event);
    if (alertDataStore.length > 50) alertDataStore.pop();

    renderAlertTable(alertDataStore);
}

function renderAlertTable(alerts) {
    const tbody = document.getElementById("alertTableBody");
    tbody.innerHTML = "";

    alerts.forEach((event, idx) => {
        const timeStr = event.timestamp.split("T")[1].substring(0, 8);
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${timeStr}</td>
            <td><strong>${event.event_id}</strong></td>
            <td>${event.source_ip} → ${event.destination_ip}</td>
            <td><span class="badge badge-accent">${event.protocol}</span></td>
            <td><strong>${event.classification}</strong></td>
            <td>${event.threat_score}</td>
            <td><span class="sev-badge sev-${event.severity}">${event.severity}</span></td>
            <td>${event.mitre_id} (${event.mitre_technique})</td>
            <td><button class="btn-inspect" onclick="inspectAlert('${event.event_id}')">Inspect</button></td>
        `;

        tbody.appendChild(tr);
    });
}

function filterAlerts(e) {
    const query = e.target.value.toLowerCase();
    const filtered = alertDataStore.filter(ev => 
        ev.source_ip.toLowerCase().includes(query) ||
        ev.classification.toLowerCase().includes(query) ||
        ev.mitre_id.toLowerCase().includes(query) ||
        ev.event_id.toLowerCase().includes(query)
    );
    renderAlertTable(filtered);
}

function fetchModelMetrics() {
    fetch("/api/metrics")
        .then(res => res.json())
        .then(data => {
            if (data.flow_model) {
                document.getElementById("m-dl-acc").innerText = (data.flow_model.accuracy * 100).toFixed(2) + "%";
                document.getElementById("m-dl-prec").innerText = (data.flow_model.precision * 100).toFixed(2) + "%";
                document.getElementById("m-dl-rec").innerText = (data.flow_model.recall * 100).toFixed(2) + "%";
                document.getElementById("m-dl-f1").innerText = (data.flow_model.f1_score * 100).toFixed(2) + "%";
                document.getElementById("m-dl-fpr").innerText = (data.flow_model.fpr * 100).toFixed(2) + "%";
            }
            if (data.arp_anomaly_model) {
                document.getElementById("m-rf-acc").innerText = (data.arp_anomaly_model.accuracy * 100).toFixed(2) + "%";
                document.getElementById("m-rf-prec").innerText = (data.arp_anomaly_model.precision * 100).toFixed(2) + "%";
                document.getElementById("m-rf-rec").innerText = (data.arp_anomaly_model.recall * 100).toFixed(2) + "%";
                document.getElementById("m-rf-f1").innerText = (data.arp_anomaly_model.f1_score * 100).toFixed(2) + "%";
                document.getElementById("m-rf-fpr").innerText = (data.arp_anomaly_model.fpr * 100).toFixed(2) + "%";
            }
        })
        .catch(err => console.error("Error fetching metrics:", err));
}

function inspectAlert(eventId) {
    const event = alertDataStore.find(e => e.event_id === eventId);
    if (!event) return;

    const modalBody = document.getElementById("modalBody");
    modalBody.innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Event ID</span>
            <span class="detail-val">${event.event_id}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Timestamp</span>
            <span class="detail-val">${event.timestamp}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Classification</span>
            <span class="detail-val" style="color: var(--color-red); font-weight: bold;">${event.classification} (${event.confidence}% Confidence)</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Threat Engine</span>
            <span class="detail-val">${event.detection_engine}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">MITRE ATT&CK</span>
            <span class="detail-val">${event.mitre_id} - ${event.mitre_technique}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Kill Chain Stage</span>
            <span class="detail-val">${event.kill_chain_stage}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">CAPEC Reference</span>
            <span class="detail-val">${event.capec_reference}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">OWASP Top 10</span>
            <span class="detail-val">${event.owasp_reference}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Description</span>
            <span class="detail-val">${event.description}</span>
        </div>
        <h4 style="margin-top: 10px; color: var(--accent-blue);">Raw ECS Payload & Feature Vectors</h4>
        <pre class="raw-json">${JSON.stringify(event, null, 2)}</pre>
    `;

    document.getElementById("alertModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("alertModal").style.display = "none";
}
