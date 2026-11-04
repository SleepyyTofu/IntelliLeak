console.log("Popup Loaded");

const status =
document.getElementById("status");

status.innerHTML = `
<div class="status-row">

<span class="green">🟢</span>

<strong>Monitoring Active</strong>

</div>

<br>

Current Protection

<ul>

<li>Sensitive Data Detection</li>

<li>Semantic Similarity Analysis</li>

<li>Leakage Risk Assessment</li>

<li>Source Attribution</li>

</ul>

Backend:

<span id="backendStatus">
Checking...
</span>
`;

fetch("http://127.0.0.1:5000")

.then(() => {

document.getElementById(
"backendStatus"
).innerHTML =

"🟢 Connected";

})

.catch(() => {

document.getElementById(
"backendStatus"
).innerHTML =

"🔴 Offline";

});