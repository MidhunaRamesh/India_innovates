import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  Cell, PieChart, Pie 
} from 'recharts';
import { 
  Activity, Trash2, Camera, Cpu, ArrowUpRight, Clock, ShieldCheck, 
  Zap, Database, Binary 
} from 'lucide-react';
import './App.css';

const App = () => {
  const [data, setData] = useState({
    last_detected: { category: "Waiting", confidence: "0%", timestamp: "00:00:00" },
    stats: { Plastic: 0, Metal: 0, Paper: 0, Organic: 0 },
    history: []
  });

  const fetchData = async () => {
    try {
      const response = await fetch('/api/status');
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Failed to fetch data", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  const chartData = Object.keys(data.stats).map(key => ({
    name: key,
    value: data.stats[key]
  }));

  const COLORS = ['#3b82f6', '#f59e0b', '#10b981', '#8b5cf6'];

  return (
    <div className="dashboard-container fade-in">
      <header className="header">
        <div className="brand">
          <div className="logo-icon"><Binary size={24} /></div>
          <h1>AI WASTE <span>NEXUS</span></h1>
        </div>
        <div className="status-panel">
          <div className="status-badge live">
            <span className="pulse"></span>
            NEURAL ENGINE ACTIVE
          </div>
          <div className="hardware-stats">
            <span><Cpu size={14} /> PI Gen 5</span>
            <span><Camera size={14} /> 4K Optical</span>
          </div>
        </div>
      </header>

      <div className="main-grid">
        {/* Real-time Monitor */}
        <section className="hero-monitor card">
          <div className="card-header">
            <Activity size={18} className="icon-accent" />
            <h3>Live Vision Detection</h3>
          </div>
          <div className="monitor-display">
            <div className="detection-focus">
              <span className="label">Classified Object</span>
              <h2 className={`glow-text cat-${data.last_detected.category.toLowerCase()}`}>
                {data.last_detected.category}
              </h2>
              <div className="meta-info">
                <div className="meta-item">
                  <Zap size={14} />
                  <span>Confidence: <b>{data.last_detected.confidence}</b></span>
                </div>
                <div className="meta-item">
                  <Clock size={14} />
                  <span>Time: <b>{data.last_detected.timestamp}</b></span>
                </div>
              </div>
            </div>
            <div className="ai-insight">
              <ShieldCheck size={20} />
              <p>AI Neural Net identifies this path as {data.last_detected.category === 'Organic' ? 'safe for composting' : 'optimal for circular recycling'}.</p>
            </div>
          </div>
        </section>

        {/* Global Statistics */}
        <section className="stats-summary">
          {Object.entries(data.stats).map(([key, val], idx) => (
            <div key={key} className={`stat-box card border-${key.toLowerCase()}`}>
              <span className="stat-label">{key}</span>
              <div className="stat-value">
                {val} 
                <small>units</small>
              </div>
              <div className="progress-bg">
                <div className="progress-fill" style={{ width: `${Math.min(val * 5, 100)}%`, backgroundColor: COLORS[idx] }}></div>
              </div>
            </div>
          ))}
        </section>

        {/* Analytics Section */}
        <section className="analytics-section card">
          <div className="card-header">
            <Database size={18} className="icon-accent" />
            <h3>Distribution Intelligence</h3>
          </div>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f111a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* Live Logs */}
        <section className="logs-panel card">
          <div className="card-header">
            <Trash2 size={18} className="icon-accent" />
            <h3>Neural Logs</h3>
          </div>
          <div className="logs-list">
            {data.history.map((log, i) => (
              <div key={i} className="log-item">
                <div className="log-marker" style={{ backgroundColor: COLORS[['Plastic', 'Metal', 'Paper', 'Organic'].indexOf(log.category)] }}></div>
                <div className="log-main">
                  <span className="log-cat">{log.category} Segregated</span>
                  <span className="log-time">{log.timestamp}</span>
                </div>
                <div className="log-conf">{log.confidence}</div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <footer className="footer">
        <p>© 2026 AI Waste Nexus | Autonomous Green Tech</p>
        <div className="footer-meta">
          <span>Latency: 42ms</span>
          <span>System Load: 24%</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
