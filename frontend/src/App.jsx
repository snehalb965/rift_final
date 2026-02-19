import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import RunForm from "./components/RunForm";
import RunSummaryCard from "./components/RunSummaryCard";
import ScorePanel from "./components/ScorePanel";
import FixesTable from "./components/FixesTable";
import CICDTimeline from "./components/CICDTimeline";
import StatusBadge from "./components/StatusBadge";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [runId, setRunId] = useState(null);
  const [runData, setRunData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [liveLog, setLiveLog] = useState([]);
  const wsRef = useRef(null);
  const logEndRef = useRef(null);

  useEffect(() => { logEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [liveLog]);

  useEffect(() => {
    if (!runId) return;
    const ws = new WebSocket(API_BASE.replace("http", "ws") + `/ws/${runId}`);
    wsRef.current = ws;
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setRunData((prev) => ({ ...prev, ...data }));
      setLiveLog((prev) => [...prev, { time: new Date().toLocaleTimeString(), event: data.event, data }]);
      if (data.event === "COMPLETED" || data.event === "ERROR") setLoading(false);
    };
    ws.onerror = () => setError("WebSocket connection failed");
    const ping = setInterval(() => { if (ws.readyState === WebSocket.OPEN) ws.send("ping"); }, 20000);
    return () => { clearInterval(ping); ws.close(); };
  }, [runId]);

  useEffect(() => {
    if (!runId || !loading) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/api/status/${runId}`);
        const data = await res.json();
        setRunData(data);
        if (data.status === "COMPLETED" || data.status === "ERROR") { setLoading(false); clearInterval(interval); }
      } catch { }
    }, 5000);
    return () => clearInterval(interval);
  }, [runId, loading]);

  const handleRunAgent = useCallback(async ({ repoUrl, teamName, leaderName }) => {
    setLoading(true); setError(null); setRunData(null); setLiveLog([]); setRunId(null);
    try {
      const res = await fetch(`${API_BASE}/api/run-agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl, team_name: teamName, leader_name: leaderName }),
      });
      if (!res.ok) { const err = await res.json(); throw new Error(err.detail || "Failed to start agent"); }
      const data = await res.json();
      setRunId(data.run_id);
      setRunData({ run_id: data.run_id, branch_name: data.branch_name, repo_url: repoUrl, team_name: teamName, leader_name: leaderName, status: "STARTING" });
    } catch (e) { setError(e.message); setLoading(false); }
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="header-logo">
            <img src="/logo.svg" alt="RIFT 2026 Logo" className="logo-icon" style={{ width: '32px', height: '32px', marginRight: '12px' }} />
            <div>
              <h1 className="logo-title">RIFT 2026</h1>
              <p className="logo-sub">Autonomous CI/CD Healing Agent</p>
            </div>
          </div>
          {runData && <StatusBadge status={runData.final_ci_status || runData.status} large />}
        </div>
      </header>

      <main className="main">
        <section className="section"><RunForm onSubmit={handleRunAgent} loading={loading} /></section>

        <AnimatePresence>
          {error && (
            <motion.div className="error-banner" initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              ⚠ {error}
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {loading && (
            <motion.section className="section" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="card live-log-card">
                <div className="card-header"><span className="pulse-dot" /><h2>Agent Live Log</h2></div>
                <div className="live-log">
                  {liveLog.length === 0 && <p className="log-waiting">Waiting for agent to start…</p>}
                  {liveLog.map((entry, i) => (
                    <div key={i} className={`log-entry log-${entry.event}`}>
                      <span className="log-time">{entry.time}</span>
                      <span className="log-event">[{entry.event}]</span>
                      <span className="log-msg">{entry.data.status || entry.data.message || JSON.stringify(entry.data).slice(0, 80)}</span>
                    </div>
                  ))}
                  <div ref={logEndRef} />
                </div>
              </div>
            </motion.section>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {runData && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="results-grid">
              <section className="section"><RunSummaryCard data={runData} /></section>
              <section className="section two-col">
                <ScorePanel score={runData.score} loading={loading} />
                {runData?.cicd_runs?.length > 0 && <CICDTimeline runs={runData.cicd_runs} maxRetries={runData.max_retries || 5} />}
              </section>
              {runData?.fixes?.length > 0 && <section className="section"><FixesTable fixes={runData.fixes} /></section>}
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="footer">RIFT 2026 Hackathon — AI/ML Track · Built with CrewAI + FastAPI + React</footer>
    </div>
  );
}