/*
    IntelliLeak Warning Dialog
*/



let dialogOpen = false;

function showWarningDialog(result, onContinue) {

    if (dialogOpen)
        return;

    dialogOpen = true;

    const old =
        document.getElementById(
            "intellileak-warning"
        );

    if (old)
        old.remove();

    const overlay =
        document.createElement("div");

    overlay.id = "intellileak-warning";

    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100vw";
    overlay.style.height = "100vh";

    overlay.style.background =
        "rgba(0,0,0,.45)";

    overlay.style.display = "flex";
    overlay.style.justifyContent = "center";
    overlay.style.alignItems = "center";

    overlay.style.zIndex = "99999999";

    let color = "#198754";
    let icon = "🟢";

    switch(result.risk_level){

        case "LOW":
            color="#ffc107";
            icon="🟡";
            break;

        case "MEDIUM":
            color="#fd7e14";
            icon="🟠";
            break;

        case "HIGH":
            color="#dc3545";
            icon="🔴";
            break;

        case "CRITICAL":
            color="#b00020";
            icon="🚨";
            break;

    }

    const source =
        result.top_source &&
        result.top_source.document !== "UNKNOWN"
            ? result.top_source.document
            : "No reliable source identified";

    const similarity =
        result.top_source &&
        result.top_source.document !== "UNKNOWN"
            ? result.top_source.similarity + "%"
            : "N/A";

    const findings =
        result.findings || [];
    
    const findingCount = 
        findings.length;

    const detectedItems =
        findings.length
            ? findings.map(item => {

                return `
                    <li style="margin-bottom:10px;">
                        <strong>${item.type}</strong><br>
                        Value: ${item.value}<br>
                        Risk:
                        <span style="
                            color:${
                                item.risk === "CRITICAL" ? "#b00020" :
                                item.risk === "HIGH" ? "#dc3545" :
                                item.risk === "MEDIUM" ? "#fd7e14" :
                                "#198754"
                            };
                            font-weight:bold;
                        ">
                            ${item.risk}
                        </span>
                    </li>
                `;

            }).join("")
            : `<li>No rule-based sensitive patterns detected.</li>`;


    const recommendations =
        result.incident &&
        result.incident.recommended_actions
            ? result.incident.recommended_actions
            : [];

    const recommendationHTML =
        recommendations.length
            ? recommendations.map(item => {

                return `<li>${item}</li>`;

            }).join("")
            : "<li>No recommendation.</li>";

    overlay.innerHTML = `

<div style="
all: initial;
font-family: Arial, sans-serif;
width:560px;
max-width:90%;
background:white;
border-radius:16px;
padding:24px;
box-shadow:0 15px 40px rgba(0,0,0,.35);

display:flex;
flex-direction:column;
max-height:85vh;
overflow:hidden;

color:#212529;
line-height:1.5;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<h2 style="
margin:0;
color:#0d6efd;
">
🛡 IntelliLeak Security Alert
</h2>

<button
id="closeDialog"
style="
border:none;
background:none;
font-size:22px;
cursor:pointer;
">
✕
</button>

</div>

<hr>

<h3 style="
margin-top:10px;
color:${color};
">
⚠ Potential Data Leakage Detected
</h3>

<p>

This prompt was flagged by IntelliLeak using <b>rule-based sensitive data detection</b> and <b>AI semantic similarity analysis</b>. Review the analysis before deciding whether to continue.

</p>


<table style="width:100%;margin-top:15px;">

<tr>

<td><strong>Risk Level</strong></td>

<td style="
color:${color};
font-weight:bold;
font-size:18px;
">

${icon} ${result.risk_level}

</td>

</tr>

<tr>

<td><strong>Risk Score</strong></td>

<td>${result.risk_score}</td>

</tr>

<tr>

<td><strong>Matched Reference</strong></td>

<td>${source}</td>

</tr>

<tr>

<td><strong>Similarity</strong></td>

<td>${similarity}</td>

</tr>

<tr>

<td><strong>Attribution</strong></td>

<td>

${
    result.top_source &&
    result.top_source.document !== "UNKNOWN"
        ? result.top_source.confidence
        : "No reliable attribution"
}

</td>

</tr>

</table>

<hr>

<div style="
flex:1;
overflow-y:auto;
padding-right:10px;
">

<strong>

Rule-Based Detection

</strong>

<p style="margin:5px 0;color:#555;">

${findingCount} sensitive pattern${findingCount === 1 ? "" : "s"} detected

</p>

<ul>

${detectedItems}

</ul>

<strong>Recommended Actions</strong>

<ul>

${recommendationHTML}

</ul>

<hr>

<p style="
font-size:12px;
color:#666;
margin-top:12px;
">

Analysis performed using IntelliLeak's hybrid detection engine:
✓ Rule-based DLP
✓ Semantic Similarity
✓ Hybrid Attribution

</p>

</div>

<div style="
display:flex;
justify-content:flex-end;
gap:15px;
margin-top:20px;
">

<button
id="cancelBtn"
style="
padding:10px 18px;
border:none;
border-radius:8px;
cursor:pointer;
background:#6c757d;
color:white;
">

Review & Edit Prompt

</button>

<button
id="continueBtn"
style="
padding:10px 18px;
border:none;
border-radius:8px;
cursor:pointer;
background:${color};
color:white;
">

Continue Submission

</button>

</div>

</div>

`;

    document.body.appendChild(
        overlay
    );

    document.body.style.overflow = "hidden";

    document
        .getElementById("closeDialog")
        .onclick = closeDialog;

    document
        .getElementById("cancelBtn")
        .onclick = closeDialog;

    document
        .getElementById("continueBtn")
        .onclick = () => {

            dialogOpen = false;

            document.body.style.overflow = "";

            overlay.remove();

            onContinue();

        };

    function closeDialog(){

        dialogOpen = false;

        document.body.style.overflow = "";

        overlay.remove();

    }

}