/*
    IntelliLeak Risk Panel
*/

console.log("risk_panel.js loaded");

let panel = null;
let panelClosed = false;

function createRiskPanel() {

    console.log("Creating IntelliLeak panel...");

    if (panelClosed)
        return;

    if (document.getElementById("intellileak-panel")) {

        panel = document.getElementById("intellileak-panel");
        return;

    }

    panel = document.createElement("div");

    panel.id = "intellileak-panel";

    panel.style.position = "fixed";
    panel.style.top = "80px";
    panel.style.right = "20px";

    panel.style.width = "280px";

    panel.style.background = "#ffffff";
    panel.style.border = "3px solid #198754";
    panel.style.borderRadius = "12px";

    panel.style.padding = "15px";

    panel.style.boxShadow =
        "0 4px 15px rgba(0,0,0,0.25)";

    panel.style.fontFamily =
        "Arial, sans-serif";

    panel.style.fontSize = "13px";

    panel.style.zIndex = "999999";

    document.body.appendChild(panel);

}

function updateRiskPanel(result) {

    console.log("updateRiskPanel() called", result);

    if (panelClosed)
        return;

    createRiskPanel();

    if (!panel)
        return;

    let color = "#198754";
    let icon = "🟢";

    switch (result.risk_level) {

        case "LOW":
            color = "#ffc107";
            icon = "🟡";
            break;

        case "MEDIUM":
            color = "#fd7e14";
            icon = "🟠";
            break;

        case "HIGH":
        case "CRITICAL":
            color = "#dc3545";
            icon = "🔴";
            break;

    }

    panel.style.borderColor = color;

    const source =
        result.top_source
            ? result.top_source.document
            : "UNKNOWN";

    const similarity =
        result.top_source
            ? result.top_source.similarity + "%"
            : "-";

    const findings =
        result.findings
            ? result.findings.length
            : 0;

    const recommendations =
        result.incident &&
        result.incident.recommended_actions
            ? result.incident.recommended_actions
            : [];

    const recommendationHTML =
        recommendations.length
            ? recommendations.map(item =>
                `<li>${item}</li>`
            ).join("")
            : "<li>No recommendations.</li>";

    const time =
        new Date().toLocaleTimeString();

    panel.innerHTML = `

    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    ">

        <h2 style="
        margin:0;
        color:#0d6efd;
        font-size:20px;
        ">
            🛡 IntelliLeak
        </h2>

        <button
            id="closePanel"
            title="Close"
            style="
            width:28px;
            height:28px;
            border:none;
            border-radius:50%;
            cursor:pointer;
            background:#f3f3f3;
            font-size:16px;
            ">
            ✕
        </button>

    </div>

    <hr>

    <p>
    <strong>${icon} Live Monitoring Active</strong>
    </p>

    <p>
    <strong>Status:</strong>

    <span style="
    color:${color};
    font-weight:bold;
    ">
    ${result.risk_level}
    </span>

    </p>

    <p>

    <strong>Risk Score:</strong>

    ${result.risk_score}

    </p>

    <p>

    <strong>Semantic Similarity:</strong>

    ${similarity}

    </p>

    <p>

    <strong>Likely Source:</strong>

    ${source}

    </p>

    <p>

    <strong>Sensitive Items:</strong>

    ${findings}

    </p>

    <p>

    <strong>Last Scan:</strong>

    ${time}

    </p>

    <hr>

    <strong>Recommendations</strong>

    <ul style="padding-left:20px;">

    ${recommendationHTML}

    </ul>

    `;

    document
        .getElementById("closePanel")
        .onclick = () => {

            panelClosed = true;

            panel.remove();

            panel = null;

        };

}

function resetRiskPanel() {

    if (!panel)
        return;

    panel.innerHTML = `
        <h2>🛡 IntelliLeak</h2>
        <hr>
        <p>Live monitoring active.</p>
        <p>Waiting for prompt...</p>
    `;

}