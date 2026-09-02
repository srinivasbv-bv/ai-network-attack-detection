let eventSource = null;
let isPaused = false;
let isDemoActive = true;
let alertDataStore = [];
let pollingInterval = null;

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
    // 1. Safe Chart Initialization
    try {
        initCharts();
    } catch (e) {
        console.warn("Chart init non-fatal exception:", e);
    }

    // 2. Fetch Model Evaluation Metrics Immediately
    fetchModelMetrics();

    // 3. Trigger initial event immediately so dashboard is populated on first load
    fetchNextEvent();

    // 4. Start continuous stream and polling fallback
    initSSE();
    startPollingFallback();

    // 5. Connect UI Event Listeners safely
    safeAddEventListener("toggleDemoBtn", "click", toggleDemoMode);
    safeAddEventListener("pauseStreamBtn", "click", toggleStream);
    safeAddEventListener("alertSearch", "input", filterAlerts);
    safeAddEventListener("severityFilter", "change", filterAlerts);
    safeAddEventListener("categoryFilter", "change", filterAlerts);
});

function safeAddEventListener(elementId, eventName, handler) {
    const elem = document.getElementById(elementId);
    if (elem) {
        elem.addEventListener(eventName, handler);
    }
}

function initCharts() {
    if (typeof Chart === 'undefined') {
        console.warn("Chart.js CDN unavailable. Analytics charts disabled safely.");
        return;
    }

    const ctxTimeline = document.getElementById("timelineChart");
    if (ctxTimeline) {
        timelineChart = new Chart(ctxTimeline.getContext("2d"), {
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
    }

    const ctxDist = document.getElementById("distributionChart");
    if (ctxDist) {
        distributionChart = new Chart(ctxDist.getContext("2d"), {
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
}

function initSSE() {
    try {
        eventSource = new EventSource("/api/stream");

        eventSource.onmessage = (e) => {
            if (isPaused) return;

            try {
                const payload = JSON.parse(e.data);
                if (payload && payload.event) {
                    processNewEvent(payload.event, payload.stats);
                }
            } catch (parseErr) {
                console.warn("SSE parse error:", parseErr);
            }
        };

        eventSource.onerror = () => {
            if (eventSource) eventSource.close();
        };
    } catch (err) {
        console.warn("SSE init error:", err);
    }
}

function startPollingFallback() {
    if (pollingInterval) return;
    pollingInterval = setInterval(() => {
        if (isPaused || !isDemoActive) return;
        fetchNextEvent();
    }, 1500);
}

function fetchNextEvent() {
    fetch("/api/next_event")
        .then(res => {
            if (!res.ok) throw new Error("HTTP error " + res.status);
            return res.json();
        })
        .then(payload => {
            if (payload && payload.event && payload.stats) {
                processNewEvent(payload.event, payload.stats);
            }
        })
        .catch(err => console.warn("Fetch event error:", err));
}

function processNewEvent(event, stats) {
    updateStats(stats);
    updatePredictionCard(event);
    addAlertToTable(event);
    updateCharts(event, stats);
    updateMitreMatrix(event);
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
            if (btn) btn.innerHTML = '<i class="fa-solid fa-toggle-on"></i> Stop Demo Mode';
            if (statusDot) statusDot.className = "status-indicator demo";
            if (statusText) statusText.innerText = "Demo Mode (Simulated)";
            if (livePill) livePill.innerHTML = '<span class="pulse-dot"></span> DEMO STREAM ACTIVE';
        } else {
            if (btn) btn.innerHTML = '<i class="fa-solid fa-toggle-off"></i> Start Demo Mode';
            if (statusDot) statusDot.className = "status-indicator online";
            if (statusText) statusText.innerText = "Online (Passive Stream)";
            if (livePill) livePill.innerHTML = '<span class="pulse-dot"></span> PASSIVE STREAM ACTIVE';
        }
    })
    .catch(err => console.error("Error toggling demo mode:", err));
}

function toggleStream() {
    isPaused = !isPaused;
    const btn = document.getElementById("pauseStreamBtn");
    if (btn) {
        if (isPaused) {
            btn.innerHTML = '<i class="fa-solid fa-play"></i> Resume Feed';
            btn.classList.add("btn-paused");
        } else {
            btn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause Feed';
            btn.classList.remove("btn-paused");
        }
    }
}

function triggerAttack(attackType) {
    const intensityElem = document.getElementById("simIntensity");
    const intensity = intensityElem ? intensityElem.value : "Medium";

    fetch("/api/trigger_attack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attack_type: attackType, intensity: intensity })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Attack simulation triggered:", data.message);
        setTimeout(fetchNextEvent, 200);
    })
    .catch(err => console.error("Error triggering attack:", err));
}

function updateStats(stats) {
    if (!stats) return;

    safeSetText("statTotalEvents", (stats.total_events || 0).toLocaleString());
    safeSetText("statNormalCount", (stats.normal_count || 0).toLocaleString());
    safeSetText("statAttackCount", (stats.attack_count || 0).toLocaleString());
    safeSetText("statThreatScore", (stats.latest_threat_score !== undefined ? stats.latest_threat_score : 0.0));

    attackCategoryCounts["Normal"] = stats.normal_count || 0;
    attackCategoryCounts["DoS"] = stats.dos_count || 0;
    attackCategoryCounts["DDoS"] = stats.ddos_count || 0;
    attackCategoryCounts["PortScan"] = stats.portscan_count || 0;
    attackCategoryCounts["BruteForce"] = stats.bruteforce_count || 0;
    attackCategoryCounts["ARP Spoofing / MITM"] = stats.mitm_count || 0;

    safeSetText("count-PortScan", `${stats.portscan_count || 0} Intercepted`);
    safeSetText("count-BruteForce", `${stats.bruteforce_count || 0} Intercepted`);
    safeSetText("count-MITM", `${stats.mitm_count || 0} Intercepted`);
    safeSetText("count-DoS", `${stats.dos_count || 0} Intercepted`);
    safeSetText("count-DDoS", `${stats.ddos_count || 0} Intercepted`);
}

function safeSetText(id, text) {
    const elem = document.getElementById(id);
    if (elem) elem.innerText = text;
}

function updatePredictionCard(event) {
    if (!event) return;

    safeSetText("predEndpoints", `${event.source_ip} ➔ ${event.destination_ip} (${event.protocol})`);
    
    const predClassElem = document.getElementById("predClass");
    if (predClassElem) {
        predClassElem.innerText = event.classification;
        predClassElem.style.color = (event.classification === "Normal") ? "var(--color-green)" : "var(--color-red)";
    }

    safeSetText("predConfidence", `${event.confidence}%`);

    const threatElem = document.getElementById("predThreatScore");
    if (threatElem) {
        threatElem.innerHTML = `${event.threat_score} <span class="sev-badge sev-${event.severity}">${event.severity}</span>`;
    }

    safeSetText("predWhyDetected", event.why_detected || "Normal baseline parameters.");

    // Key Features Chips
    const flow = event.raw_features?.flow || {};
    const arp = event.raw_features?.protocol || {};

    const pkts_s = flow.flow_packets_s !== undefined ? `${flow.flow_packets_s.toFixed(0)}/s` : "--";
    const duration = flow.flow_duration !== undefined ? `${flow.flow_duration.toFixed(0)}ms` : "--";
    const dst_port = flow.dst_port !== undefined ? flow.dst_port : "--";
    const syn_cnt = flow.syn_flag_count !== undefined ? flow.syn_flag_count : "--";
    const failed_auth = flow.failed_auth_attempts !== undefined ? flow.failed_auth_attempts : "--";
    const arp_ratio = arp.arp_reply_req_ratio !== undefined ? arp.arp_reply_req_ratio.toFixed(1) : "--";

    const keyFeatsElem = document.getElementById("predKeyFeatures");
    if (keyFeatsElem) {
        keyFeatsElem.innerHTML = `
            <span class="chip">Packet Rate: ${pkts_s}</span>
            <span class="chip">Flow Duration: ${duration}</span>
            <span class="chip">Dst Port: ${dst_port}</span>
            <span class="chip">SYN Flags: ${syn_cnt}</span>
            <span class="chip">Auth Failures: ${failed_auth}</span>
            <span class="chip">ARP Reply Ratio: ${arp_ratio}</span>
        `;
    }
}

function updateCharts(event, stats) {
    if (!event || !event.timestamp) return;

    if (timelineChart) {
        try {
            const timestampLabel = event.timestamp.split("T")[1].substring(0, 8);
            timelineChart.data.labels.push(timestampLabel);
            timelineChart.data.datasets[0].data.push(event.threat_score);

            if (timelineChart.data.labels.length > 20) {
                timelineChart.data.labels.shift();
                timelineChart.data.datasets[0].data.shift();
            }
            timelineChart.update();
        } catch (e) {
            console.warn("Timeline chart update error:", e);
        }
    }

    if (distributionChart) {
        try {
            distributionChart.data.datasets[0].data = [
                stats.normal_count || 0,
                stats.dos_count || 0,
                stats.ddos_count || 0,
                stats.portscan_count || 0,
                stats.bruteforce_count || 0,
                stats.mitm_count || 0
            ];
            distributionChart.update();
        } catch (e) {
            console.warn("Distribution chart update error:", e);
        }
    }
}

function updateMitreMatrix(event) {
    if (!event) return;
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
    if (!event) return;
    alertDataStore.unshift(event);
    if (alertDataStore.length > 50) alertDataStore.pop();

    filterAlerts();
}

function renderAlertTable(alerts) {
    const tbody = document.getElementById("alertTableBody");
    if (!tbody) return;

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
    const searchElem = document.getElementById("alertSearch");
    const sevElem = document.getElementById("severityFilter");
    const catElem = document.getElementById("categoryFilter");

    const searchQuery = (searchElem ? searchElem.value : "").toLowerCase();
    const sevFilter = sevElem ? sevElem.value : "ALL";
    const catFilter = catElem ? catElem.value : "ALL";

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
                safeSetText("m-dl-acc", (data.flow_model.accuracy * 100).toFixed(2) + "%");
                safeSetText("m-dl-prec", (data.flow_model.precision * 100).toFixed(2) + "%");
                safeSetText("m-dl-rec", (data.flow_model.recall * 100).toFixed(2) + "%");
                safeSetText("m-dl-f1", (data.flow_model.f1_score * 100).toFixed(2) + "%");
                safeSetText("m-dl-fpr", (data.flow_model.fpr * 100).toFixed(2) + "%");
                safeSetText("m-dl-fnr", ((data.flow_model.fnr !== undefined ? data.flow_model.fnr : (1 - data.flow_model.recall)) * 100).toFixed(2) + "%");

                renderConfusionMatrixTable("dlCmContainer", data.flow_model.confusion_matrix, data.flow_model.classes);
            }

            if (data.arp_anomaly_model) {
                safeSetText("m-rf-acc", (data.arp_anomaly_model.accuracy * 100).toFixed(2) + "%");
                safeSetText("m-rf-prec", (data.arp_anomaly_model.precision * 100).toFixed(2) + "%");
                safeSetText("m-rf-rec", (data.arp_anomaly_model.recall * 100).toFixed(2) + "%");
                safeSetText("m-rf-f1", (data.arp_anomaly_model.f1_score * 100).toFixed(2) + "%");
                safeSetText("m-rf-fpr", (data.arp_anomaly_model.fpr * 100).toFixed(2) + "%");
                safeSetText("m-rf-fnr", ((data.arp_anomaly_model.fnr !== undefined ? data.arp_anomaly_model.fnr : (1 - data.arp_anomaly_model.recall)) * 100).toFixed(2) + "%");

                renderConfusionMatrixTable("rfCmContainer", data.arp_anomaly_model.confusion_matrix, data.arp_anomaly_model.classes);
            }
        })
        .catch(err => console.error("Error fetching metrics:", err));
}

function renderConfusionMatrixTable(containerId, cm, classes) {
    const container = document.getElementById(containerId);
    if (!container || !cm || !classes) return;

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
    if (!modalBody) return;

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

        <div class="cmd-box">
            <h5><i class="fa-solid fa-terminal"></i> Active Firewall & Automated Mitigation Command</h5>
            <pre class="cmd-code">${event.active_mitigation_cmd || '# No blocking command needed'}</pre>
        </div>

        <h4 style="margin-top: 14px; color: var(--accent-blue);">Raw Elastic Common Schema (ECS) Payload</h4>
        <pre class="raw-json">${JSON.stringify(event, null, 2)}</pre>
    `;

    const modal = document.getElementById("alertModal");
    if (modal) modal.style.display = "flex";
}

function closeModal() {
    const modal = document.getElementById("alertModal");
    if (modal) modal.style.display = "none";
}
