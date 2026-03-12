from flask import Flask, render_template_string, jsonify
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Waste Nexus | Intelligent Segregation</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0b10;
            --card-bg: #151921;
            --accent: #00f2ff;
            --plastic: #3b82f6;
            --metal: #f59e0b;
            --paper: #10b981;
            --organic: #8b5cf6;
            --text: #e2e8f0;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Outfit', sans-serif; 
            background: var(--bg); 
            color: var(--text); 
            overflow-x: hidden;
            min-height: 100vh;
        }

        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
        }

        .logo {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--accent), #7000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }

        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(0, 242, 255, 0.1);
            border: 1px solid rgba(0, 242, 255, 0.3);
            color: var(--accent);
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            animation: pulse-glow 2s infinite;
        }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(0, 242, 255, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(0, 242, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 242, 255, 0); }
        }

        /* Hero Section */
        .grid-main {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 24px;
        }

        .hero-card {
            background: var(--card-bg);
            border-radius: 24px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 300px;
        }

        .hero-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(112, 0, 255, 0.2) 0%, transparent 70%);
            z-index: 0;
        }

        .hero-content { position: relative; z-index: 1; }
        .hero-label { color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 2px; }
        .hero-val { font-size: 3.5rem; font-weight: 800; margin-bottom: 8px; }
        .hero-meta { display: flex; gap: 24px; color: #94a3b8; }
        .hero-meta span { display: flex; align-items: center; gap: 6px; }

        /* Stats Grid */
        .stats-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-top: 24px;
        }

        .stat-card {
            background: var(--card-bg);
            padding: 24px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease;
        }

        .stat-card:hover { transform: translateY(-5px); border-borderColor: rgba(255, 255, 255, 0.15); }
        .stat-label { font-size: 0.9rem; color: #94a3b8; margin-bottom: 12px; }
        .stat-val { font-size: 2rem; font-weight: 700; }
        
        .c-plastic { border-left: 4px solid var(--plastic); }
        .c-metal { border-left: 4px solid var(--metal); }
        .c-paper { border-left: 4px solid var(--paper); }
        .c-organic { border-left: 4px solid var(--organic); }

        /* History & Insights */
        .side-panel { display: flex; flex-direction: column; gap: 24px; }
        .panel { 
            background: var(--card-bg); 
            border-radius: 24px; 
            padding: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.05); 
        }

        .panel-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 20px; display: flex; justify-content: space-between; }
        
        .history-list { list-style: none; }
        .history-item {
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .history-item:last-child { border: none; }
        .h-cat { font-weight: 600; font-size: 0.95rem; }
        .h-time { font-size: 0.8rem; color: #64748b; }
        .h-conf { font-size: 0.8rem; background: rgba(255, 255, 255, 0.05); padding: 2px 6px; border-radius: 4px; }

        .chart-container { margin-top: 24px; height: 300px; }

        @media (max-width: 1000px) {
            .grid-main { grid-template-columns: 1fr; }
            .stats-row { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <div class="logo">AI WASTE NEXUS</div>
            <div class="status-badge">
                <div class="pulse"></div> RPi ACTIVE
            </div>
        </header>

        <main class="grid-main">
            <div class="content">
                <div class="hero-card">
                    <div class="hero-content">
                        <div class="hero-label">Current Classification</div>
                        <div class="hero-val" id="current_cat">Ready</div>
                        <div class="hero-meta">
                            <span> Confidence: <b id="current_conf">N/A</b></span>
                            <span> Time: <b id="current_time">00:00:00</b></span>
                        </div>
                    </div>
                </div>

                <div class="stats-row">
                    <div class="stat-card c-plastic">
                        <div class="stat-label">Plastic</div>
                        <div class="stat-val" id="s_plastic">0</div>
                    </div>
                    <div class="stat-card c-metal">
                        <div class="stat-label">Metal</div>
                        <div class="stat-val" id="s_metal">0</div>
                    </div>
                    <div class="stat-card c-paper">
                        <div class="stat-label">Paper</div>
                        <div class="stat-val" id="s_paper">0</div>
                    </div>
                    <div class="stat-card c-organic">
                        <div class="stat-label">Organic</div>
                        <div class="stat-val" id="s_organic">0</div>
                    </div>
                </div>

                <div class="panel chart-container">
                    <div class="panel-title">Distribution Analytics</div>
                    <canvas id="myChart"></canvas>
                </div>
            </div>

            <aside class="side-panel">
                <div class="panel">
                    <div class="panel-title">Live Log</div>
                    <ul class="history-list" id="history">
                        <li class="history-item">System initialized...</li>
                    </ul>
                </div>
                
                <div class="panel" style="background: linear-gradient(135deg, #1e1b4b, #151921);">
                    <div class="panel-title">AI Insights</div>
                    <p id="insight_text" style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
                        Analyzing patterns... Detection of Plastic items has increased by 12% in the last hour.
                    </p>
                </div>
            </aside>
        </main>
    </div>

    <script>
        let myChart;
        
        function initChart() {
            const ctx = document.getElementById('myChart').getContext('2d');
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Plastic', 'Metal', 'Paper', 'Organic'],
                    datasets: [{
                        label: 'Waste Volume',
                        data: [0, 0, 0, 0],
                        backgroundColor: ['#3b82f6', '#f59e0b', '#10b981', '#8b5cf6'],
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }

        function updateUI() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    if (data.last_detected) {
                        document.getElementById('current_cat').innerText = data.last_detected.category;
                        document.getElementById('current_conf').innerText = data.last_detected.confidence;
                        document.getElementById('current_time').innerText = data.last_detected.timestamp;
                    }
                    
                    if (data.stats) {
                        document.getElementById('s_plastic').innerText = data.stats.Plastic;
                        document.getElementById('s_metal').innerText = data.stats.Metal;
                        document.getElementById('s_paper').innerText = data.stats.Paper;
                        document.getElementById('s_organic').innerText = data.stats.Organic;
                        
                        myChart.data.datasets[0].data = [
                            data.stats.Plastic, data.stats.Metal, 
                            data.stats.Paper, data.stats.Organic
                        ];
                        myChart.update();

                        // Generate AI insight
                        const counts = Object.values(data.stats);
                        const max = Math.max(...counts);
                        if (max > 0) {
                            const common = Object.keys(data.stats).find(key => data.stats[key] === max);
                            document.getElementById('insight_text').innerText = `Primary waste detected: ${common}. Suggesting ${common} recycling priority optimization.`;
                        }
                    }

                    if (data.history) {
                        const hList = document.getElementById('history');
                        hList.innerHTML = data.history.map(item => `
                            <li class="history-item">
                                <div>
                                    <div class="h-cat">${item.category}</div>
                                    <div class="h-time">${item.timestamp}</div>
                                </div>
                                <div class="h-conf">${item.confidence}</div>
                            </li>
                        `).join('');
                    }
                });
        }

        initChart();
        setInterval(updateUI, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    state_file = "system_state.json"
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                return jsonify(json.load(f))
        except:
            pass
    
    # Fallback initial state
    return jsonify({
        "last_detected": {"category": "Waiting", "confidence": "0%", "timestamp": "00:00:00"},
        "stats": {"Plastic": 0, "Metal": 0, "Paper": 0, "Organic": 0},
        "history": []
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
