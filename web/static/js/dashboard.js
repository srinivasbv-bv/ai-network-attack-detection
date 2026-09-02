let eventSource = null;
let isPaused = false;
let isDemoActive = true;
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

    document.getElementById("toggleDemoBtn").addEventListener("click", toggleDemoMode);
    document.getElementById("pauseStreamBtn").addEventListener("click", toggleStream);
    document.getElementById("alertSearch").addEventListener("input", filterAlerts);
    document.getElementById("severityFilter").addEventListener("change", filterAlerts);
    document.getElementById("categoryFilter").addEventListener("change", filterAlerts);
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
                backgroundColor: "rgba(0, 242, 254, 0.12)",
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
    try {
        eventSource = new EventSource("/api/stream");

        eventSource.onmessage = (e) => {
            if (isPaused) return;

            const payload = JSON.parse(e.data);
            const event = payload.event;
            const stats = payload.stats;

            updateStats(stats);
            updatePredictionCard(event);
            addAlertToTable(event);
            updateCharts(event, stats);
            updateMitreMatrix(event);
        };

        eventSource.onerror = () => {
            console.warn("SSE stream interrupted. Switching to polling fallback...");
            if (eventSource) eventSource.close();
            startPollingFallback();
        };
    } catch (err) {
        console.warn("SSE init error. Using polling fallback...");
        startPollingFallback();
    }
}

let pollingInterval = null;
function startPollingFallback() {
    if (pollingInterval) return;
    pollingInterval = setInterval(() => {
        if (isPaused) return;
        fetch("/api/next_event")
            .then(res => res.json())
            .then(payload => {
                if (payload.event && payload.stats) {
                    updateStats(payload.stats);
                    updatePredictionCard(payload.event);
                    addAlertToTable(payload.event);
                    updateCharts(payload.event, payload.stats);
                    updateMitreMatrix(payload.event);
                }
            })
            .catch(err => console.warn("Polling fallback error:", err));
    }, 1500);
}

function toggleDemoMode() {
    isDemoActive = !isDemoActive;
    fetch("/api/toggle_demo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled: isDemoActive })
    })
    .then(res => res.json())
    .then(data => {
        const btn = document.getElementById("toggleDemoBtn");
        const statusDot = document.getElementById("statusDot");
        const statusText = document.getElementById("statusText");
        const livePill = document.getElementById("livePill");

        if (data.demo_mode) {
            btn.innerHTML = '<i class="fa-solid fa-toggle-on"></i> Stop Demo Mode';
            statusDot.className = "status-indicator demo";
            statusText.innerText = "Demo Mode (Simulated)";
            livePill.innerHTML = '<span class="pulse-dot"></span> DEMO STREAM ACTIVE';
        } else {
            btn.innerHTML = '<i class="fa-solid fa-toggle-off"></i> Start Demo Mode';
            statusDot.className = "status-indicator online";
            statusText.innerText = "Online (Passive Stream)";
            livePill.innerHTML = '<span class="pulse-dot"></span> PASSIVE STREAM ACTIVE';
        }
    })
    .catch(err => console.error("Error toggling demo mode:", err));
}

function toggleStream() {
    isPaused = !isPaused;
    const btn = document.getElementById("pauseStreamBtn");
    if (isPaused) {
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Resume Feed';
        btn.classList.add("btn-paused");
    } else {
        btn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause Feed';
        btn.classList.remove("btn-paused");
    }
}

function triggerAttack(attackType) {
    const intensity = document.getElementById("simIntensity").value || "Medium";
    fetch("/api/trigger_attack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attack_type: attackType, intensity: intensity })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Attack simulation triggered:", data.message);
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

function updatePredictionCard(event) {
    document.getElementById("predEndpoints").innerText = `${event.source_ip} ➔ ${event.destination_ip} (${event.protocol})`;
    
    const predClassElem = document.getElementById("predClass");
    predClassElem.innerText = event.classification;
    if (event.classification === "Normal") {
        predClassElem.style.color = "var(--color-green)";
    } else {
        predClassElem.style.color = "var(--color-red)";
    }

    document.getElementById("predConfidence").innerText = `${event.confidence}%`;
    document.getElementById("predThreatScore").innerHTML = `${event.threat_score} <span class="sev-badge sev-${event.severity}">${event.severity}</span>`;

    document.getElementById("predWhyDetected").innerText = event.why_detected || "Normal baseline parameters.";

    // Key Features Chips
    const flow = event.raw_features?.flow || {};
    const arp = event.raw_features?.protocol || {};

    const pkts_s = flow.flow_packets_s !== undefined ? `${flow.flow_packets_s.toFixed(0)}/s` : "--";
    const duration = flow.flow_duration !== undefined ? `${flow.flow_duration.toFixed(0)}ms` : "--";
    const dst_port = flow.dst_port !== undefined ? flow.dst_port : "--";
    const syn_cnt = flow.syn_flag_count !== undefined ? flow.syn_flag_count : "--";
    const failed_auth = flow.failed_auth_attempts !== undefined ? flow.failed_auth_attempts : "--";
    const arp_ratio = arp.arp_reply_req_ratio !== undefined ? arp.arp_reply_req_ratio.toFixed(1) : "--";

    document.getElementById("predKeyFeatures").innerHTML = `
        <span class="chip">Packet Rate: ${pkts_s}</span>
        <span class="chip">Flow Duration: ${duration}</span>
        <span class="chip">Dst Port: ${dst_port}</span>
        <span class="chip">SYN Flags: ${syn_cnt}</span>
        <span class="chip">Auth Failures: ${failed_auth}</span>
        <span class="chip">ARP Reply Ratio: ${arp_ratio}</span>
    `;
}

function updateCharts(event, stats) {
    const timestampLabel = event.timestamp.split("T")[1].substring(0, 8);
    timelineChart.data.labels.push(timestampLabel);
    timelineChart.data.datasets[0].data.push(event.threat_score);

    if (timelineChart.data.labels.length > 20) {
        timelineChart.data.labels.shift();
        timelineChart.data.datasets[0].data.shift();
    }
    timelineChart.update();

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

    filterAlerts();
}

function renderAlertTable(alerts) {
    const tbody = document.getElementById("alertTableBody");
    tbody.innerHTML = "";

    if (alerts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">No alerts matching current filters.</td></tr>';
        return;
    }

    alerts.forEach((event) => {
        const timeStr = event.timestamp.split("T")[1].substring(0, 8);
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${timeStr}</td>
            <td><strong>${event.event_id}</strong></td>
            <td>${event.source_ip} ➔ ${event.destination_ip}</td>
            <td><span class="badge badge-accent">${event.protocol}</span></td>
            <td><strong>${event.classification}</strong></td>
            <td>${event.threat_score}</td>
            <td><span class="sev-badge sev-${event.severity}">${event.severity}</span></td>
            <td>${event.mitre_id} (${event.mitre_technique})</td>
            <td><button class="btn-inspect" onclick="inspectAlert('${event.event_id}')">Investigate</button></td>
        `;

        tbody.appendChild(tr);
    });
}

function filterAlerts() {
    const searchQuery = (document.getElementById("alertSearch").value || "").toLowerCase();
    const sevFilter = document.getElementById("severityFilter").value;
    const catFilter = document.getElementById("categoryFilter").value;

    const filtered = alertDataStore.filter(ev => {
        const matchesSearch = 
            ev.source_ip.toLowerCase().includes(searchQuery) ||
            ev.destination_ip.toLowerCase().includes(searchQuery) ||
            ev.classification.toLowerCase().includes(searchQuery) ||
            ev.mitre_id.toLowerCase().includes(searchQuery) ||
            ev.event_id.toLowerCase().includes(searchQuery);

        const matchesSev = (sevFilter === "ALL" || ev.severity === sevFilter);
        const matchesCat = (catFilter === "ALL" || ev.classification === catFilter);

        return matchesSearch && matchesSev && matchesCat;
    });

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
                document.getElementById("m-dl-fnr").innerText = ((data.flow_model.fnr || (1 - data.flow_model.recall)) * 100).toFixed(2) + "%";

                renderConfusionMatrixTable("dlCmContainer", data.flow_model.confusion_matrix, data.flow_model.classes);
            }

            if (data.arp_anomaly_model) {
                document.getElementById("m-rf-acc").innerText = (data.arp_anomaly_model.accuracy * 100).toFixed(2) + "%";
                document.getElementById("m-rf-prec").innerText = (data.arp_anomaly_model.precision * 100).toFixed(2) + "%";
                document.getElementById("m-rf-rec").innerText = (data.arp_anomaly_model.recall * 100).toFixed(2) + "%";
                document.getElementById("m-rf-f1").innerText = (data.arp_anomaly_model.f1_score * 100).toFixed(2) + "%";
                document.getElementById("m-rf-fpr").innerText = (data.arp_anomaly_model.fpr * 100).toFixed(2) + "%";
                document.getElementById("m-rf-fnr").innerText = ((data.arp_anomaly_model.fnr || (1 - data.arp_anomaly_model.recall)) * 100).toFixed(2) + "%";

                renderConfusionMatrixTable("rfCmContainer", data.arp_anomaly_model.confusion_matrix, data.arp_anomaly_model.classes);
            }
        })
        .catch(err => console.error("Error fetching metrics:", err));
}

function renderConfusionMatrixTable(containerId, cm, classes) {
    const container = document.getElementById(containerId);
    if (!cm || !classes) return;

    let html = '<table class="cm-table"><thead><tr><th>Actual \\ Pred</th>';
    classes.forEach(c => { html += `<th>${c}</th>`; });
    html += '</tr></thead><tbody>';

    cm.forEach((row, i) => {
        html += `<tr><td><strong>${classes[i]}</strong></td>`;
        row.forEach((val, j) => {
            const isCorrect = (i === j);
            const cellClass = isCorrect ? 'cm-correct' : (val > 0 ? 'cm-error' : '');
            html += `<td class="${cellClass}">${val}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

function inspectAlert(eventId) {
    const event = alertDataStore.find(e => e.event_id === eventId);
    if (!event) return;

    const modalBody = document.getElementById("modalBody");
    modalBody.innerHTML = `
        <div class="lifecycle-bar">
            <div class="step step-done"><i class="fa-solid fa-circle-check"></i> 1. Detected</div>
            <div class="step step-done"><i class="fa-solid fa-circle-check"></i> 2. Classified</div>
            <div class="step step-active"><i class="fa-solid fa-circle-play"></i> 3. Investigated</div>
            <div class="step"><i class="fa-solid fa-clock"></i> 4. Recommended Response</div>
            <div class="step"><i class="fa-solid fa-shield"></i> 5. Verified</div>
        </div>

        <div class="detail-row">
            <span class="detail-label">Event ID</span>
            <span class="detail-val"><strong>${event.event_id}</strong></span>
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
            <span class="detail-label">Threat Score & Severity</span>
            <span class="detail-val">${event.threat_score} <span class="sev-badge sev-${event.severity}">${event.severity}</span> (${event.score_range || ''})</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Detection Engine</span>
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
            <span class="detail-label">CAPEC / OWASP</span>
            <span class="detail-val">${event.capec_reference} | ${event.owasp_reference}</span>
        </div>

        <div class="why-box">
            <h5><i class="fa-solid fa-circle-question"></i> Why Was This Detected? (Feature-Based Reasoning)</h5>
            <p>${event.why_detected || event.description}</p>
        </div>

        <div class="response-box">
            <h5><i class="fa-solid fa-user-shield"></i> Recommended Response (Analyst Guidance)</h5>
            <p>${event.recommended_response || 'No immediate response required.'}</p>
        </div>

        <h4 style="margin-top: 14px; color: var(--accent-blue);">Raw Elastic Common Schema (ECS) Payload</h4>
        <pre class="raw-json">${JSON.stringify(event, null, 2)}</pre>
    `;

    document.getElementById("alertModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("alertModal").style.display = "none";
}
