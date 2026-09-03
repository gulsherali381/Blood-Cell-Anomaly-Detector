const API_url = "https://gulsherali381--blood-cell-anomaly-detector-fastapi-app.modal.run";
let history = [];
let lastBulkResults = [];

// Tab switching logic
function showTab(event, tabName) {
    document.querySelectorAll(".tab-content").forEach(tab => tab.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));

    document.getElementById(tabName).classList.add("active");
    event.currentTarget.classList.add("active");

    if (tabName === "log") {
        renderLog();
    } else if (tabName === "insights") {
        loadInsights();
    }
}

// Run Single Scan
async function runScan() {
    const threshold = parseFloat(document.getElementById("threshold").value);
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = `
        <div class="result-card" style="border-color: #8715DB;">
            <p style="color: #dcd0ea; font-size: 1.1rem;">🔄 Analyzing cell data...</p>
        </div>
    `;

    try {
        await fetch(`${API_url}/set-threshold?value=${threshold}`);
    } catch (e) {
        console.log("Threshold update warning:", e);
    }

    const payload = {
        cell_type: document.getElementById("cell_type").value,
        cell_diameter_um: parseFloat(document.getElementById("cell_diameter_um").value),
        nucleus_area_pct: parseFloat(document.getElementById("nucleus_area_pct").value),
        chromatin_density: parseFloat(document.getElementById("chromatin_density").value),
        cytoplasm_ratio: parseFloat(document.getElementById("cytoplasm_ratio").value),
        circularity: parseFloat(document.getElementById("circularity").value),
        eccentricity: parseFloat(document.getElementById("eccentricity").value),
        granularity_score: parseFloat(document.getElementById("granularity_score").value),
        lobularity_score: parseFloat(document.getElementById("lobularity_score").value),
        membrane_smoothness: parseFloat(document.getElementById("membrane_smoothness").value),
        cell_area_px: parseInt(document.getElementById("cell_area_px").value),
        perimeter_px: parseInt(document.getElementById("perimeter_px").value),
        mean_r: parseInt(document.getElementById("mean_r").value),
        mean_g: parseInt(document.getElementById("mean_g").value),
        mean_b: parseInt(document.getElementById("mean_b").value),
        stain_intensity: parseFloat(document.getElementById("stain_intensity").value)
    };

    const patientName = document.getElementById("patient_name").value;

    try {
        const response = await fetch(`${API_url}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const result = await response.json();
            const prediction = result.Prediction;
            const score = result.Score;
            const color = prediction === "Anomaly" ? "#ff4b4b" : "#00c853";

            resultDiv.innerHTML = `
                <div class="result-card">
                    <h3 style="color:${color}">${prediction.toUpperCase()}</h3>
                    <p style="font-size:2rem; font-weight:bold;">${score.toFixed(4)}</p>
                    <p>Anomaly Score</p>
                </div>
            `;

            history.push({
                timestamp: new Date().toLocaleTimeString(),
                patient: patientName,
                cell_type: payload.cell_type,
                prediction: prediction,
                score: score
            });
        } else {
            resultDiv.innerHTML = `<p style="color: #ff4b4b;">Server error during prediction.</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: #ff4b4b;">Connection failed. Make sure backend is running.</p>`;
        console.error(error);
    }
}

// Bulk Scan Implementation with Download Button
function runBulkScan() {
    const fileInput = document.getElementById("csvFile");
    const bulkResultDiv = document.getElementById("bulkResult");

    if (!fileInput || fileInput.files.length === 0) {
        alert("Please select a CSV file first!");
        return;
    }

    const file = fileInput.files[0];
    bulkResultDiv.innerHTML = `<p style="color: #dcd0ea;">⚡ Processing bulk records...</p>`;

    Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        complete: async function(results) {
            const rows = results.data.filter(row => row.cell_type);

            if (rows.length === 0) {
                bulkResultDiv.innerHTML = `<p style="color: #ff4b4b;">CSV file is empty or formatted incorrectly.</p>`;
                return;
            }

            const payloadRows = rows.map(row => ({
                cell_type: row.cell_type || "Neutrophil",
                cell_diameter_um: parseFloat(row.cell_diameter_um) || 10.0,
                nucleus_area_pct: parseFloat(row.nucleus_area_pct) || 50.0,
                chromatin_density: parseFloat(row.chromatin_density) || 0.4,
                cytoplasm_ratio: parseFloat(row.cytoplasm_ratio) || 0.4,
                circularity: parseFloat(row.circularity) || 0.8,
                eccentricity: parseFloat(row.eccentricity) || 0.4,
                granularity_score: parseFloat(row.granularity_score) || 2.0,
                lobularity_score: parseFloat(row.lobularity_score) || 3.0,
                membrane_smoothness: parseFloat(row.membrane_smoothness) || 0.8,
                cell_area_px: parseInt(row.cell_area_px) || 300,
                perimeter_px: parseInt(row.perimeter_px) || 60,
                mean_r: parseInt(row.mean_r) || 200,
                mean_g: parseInt(row.mean_g) || 150,
                mean_b: parseInt(row.mean_b) || 180,
                stain_intensity: parseFloat(row.stain_intensity) || 0.5
            }));

            try {
                const response = await fetch(`${API_url}/predict-bulk`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ rows: payloadRows })
                });

                if (response.ok) {
                    const data = await response.json();
                    const predictions = data.results;

                    lastBulkResults = payloadRows.map((row, index) => ({
                        ...row,
                        Prediction: predictions[index].Prediction,
                        Score: predictions[index].Score
                    }));

                    let outputHtml = `
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                            <h3>Bulk Scan Results (${predictions.length} rows processed)</h3>
                            <button onclick="downloadCSV()" style="margin-top:0; background-color: #00c853;">📥 Download Results CSV</button>
                        </div>
                        <table><tr><th>#</th><th>Cell Type</th><th>Prediction</th><th>Score</th></tr>`;

                    predictions.forEach((res, index) => {
                        let cellType = payloadRows[index].cell_type;
                        let color = res.Prediction === 'Anomaly' ? '#ff4b4b' : '#00c853';
                        outputHtml += `<tr><td>${index + 1}</td><td>${cellType}</td><td style="color:${color}; font-weight:bold;">${res.Prediction}</td><td>${res.Score.toFixed(4)}</td></tr>`;
                    });

                    outputHtml += `</table>`;
                    bulkResultDiv.innerHTML = outputHtml;
                } else {
                    bulkResultDiv.innerHTML = `<p style="color: #ff4b4b;">Server error during bulk processing.</p>`;
                }
            } catch (err) {
                bulkResultDiv.innerHTML = `<p style="color: #ff4b4b;">Failed to connect to backend server.</p>`;
                console.error(err);
            }
        },
        error: function(err) {
            bulkResultDiv.innerHTML = `<p style="color: #ff4b4b;">Error parsing CSV file.</p>`;
        }
    });
}

// Download CSV file function
function downloadCSV() {
    if (lastBulkResults.length === 0) return;

    let csvContent = "data:text/csv;charset=utf-8,";
    const headers = Object.keys(lastBulkResults[0]);
    csvContent += headers.join(",") + "\r\n";

    lastBulkResults.forEach(row => {
        const values = headers.map(header => row[header]);
        csvContent += values.join(",") + "\r\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "blood_cell_scan_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Load Insights View with Chart.js Graph
async function loadInsights() {
    const insightsDiv = document.getElementById("insightsResult");

    try {
        const response = await fetch(`${API_url}/insights`);
        if (response.ok) {
            const data = await response.json();

            insightsDiv.innerHTML = `
                <h3>📊 Dataset Overview</h3>
                <p><b>Total Records in Training Dataset:</b> ${data.total_records}</p>
                <p><b>Features Analyzed:</b> 16 Cellular Metrics | <b>Model:</b> Isolation Forest</p>
                <h3 style="margin-top: 25px;">🧬 Cell Type Distribution Graph</h3>
                <div style="background: #0f021a; padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <canvas id="cellChart" style="max-height: 400px;"></canvas>
                </div>
            `;

            const ctx = document.getElementById('cellChart').getContext('2d');
            const labels = Object.keys(data.cell_distribution);
            const values = Object.values(data.cell_distribution);

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sample Count',
                        data: values,
                        backgroundColor: '#8715DB',
                        borderColor: '#a83232',
                        borderWidth: 1,
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    },
                    scales: {
                        x: { ticks: { color: 'white' }, grid: { color: '#333' } },
                        y: { ticks: { color: 'white' }, grid: { color: '#333' } }
                    }
                }
            });

        } else {
            insightsDiv.innerHTML = `<p style="color: #ff4b4b;">Failed to load insights data.</p>`;
        }
    } catch (e) {
        insightsDiv.innerHTML = `<p style="color: #ff4b4b;">Connection error while fetching insights.</p>`;
        console.error(e);
    }
}

// Render History Log
function renderLog() {
    const logDiv = document.getElementById("logResult");

    if (history.length === 0) {
        logDiv.innerHTML = "<p>No scans have been performed yet.</p>";
        return;
    }

    let avgScore = history.reduce((sum, h) => sum + h.score, 0) / history.length;

    let html = `
        <p><b>Total Scans:</b> ${history.length} | <b>Avg Score:</b> ${avgScore.toFixed(4)}</p>
        <table>
            <tr><th>Time</th><th>Patient</th><th>Cell Type</th><th>Prediction</th><th>Score</th></tr>
    `;

    history.forEach(h => {
        html += `<tr><td>${h.timestamp}</td><td>${h.patient}</td><td>${h.cell_type}</td><td>${h.prediction}</td><td>${h.score.toFixed(4)}</td></tr>`;
    });

    html += "</table>";
    logDiv.innerHTML = html;
}