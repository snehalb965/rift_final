// ── StatusBadge ──
export function StatusBadge({ status, large }) {
  const icons = { PASSED: "✓", COMPLETED: "✓", FAILED: "✗", ERROR: "✗", STARTING: "◌", RUNNING: "◌", CLONING: "◌", UNKNOWN: "?", TIMEOUT: "⏱" };
  return <span className={`badge badge-${status} ${large ? "large" : ""}`}>{icons[status] || "●"} {status}</span>;
}

// ── RunSummaryCard ──
export function RunSummaryCard({ data }) {
  const duration = () => {
    if (!data.started_at || !data.completed_at) return "—";
    const s = (new Date(data.completed_at) - new Date(data.started_at)) / 1000;
    return s < 60 ? `${Math.round(s)}s` : `${Math.floor(s / 60)}m ${Math.round(s % 60)}s`;
  };
  const items = [
    { label: "Repository", value: data.repo_url, cls: "mono" },
    { label: "Team", value: data.team_name || "—" },
    { label: "Leader", value: data.leader_name || "—" },
    { label: "Branch Created", value: data.branch_name || "—", cls: "accent mono" },
    { label: "Failures Detected", value: data.total_fixes ?? "—", cls: "big" },
    { label: "Fixes Applied", value: data.total_fixes ?? "—", cls: "big" },
    { label: "Time Taken", value: duration(), cls: "big" },
    { label: "CI/CD Status", value: <StatusBadge status={data.final_ci_status || data.status || "UNKNOWN"} /> },
    { label: "Run ID", value: data.run_id || "—", cls: "mono" },
  ];
  return (
    <div className="card">
      <div className="card-header"><h2>📋 Run Summary</h2></div>
      <div className="summary-grid">
        {items.map((item, i) => (
          <div key={i} className="summary-item">
            <div className="summary-label">{item.label}</div>
            <div className={`summary-value ${item.cls || ""}`}>{item.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── ScorePanel ──
export function ScorePanel({ score, loading }) {
  if (!score && !loading) return (
    <div className="card">
      <div className="card-header"><h2>🏆 Score</h2></div>
      <p style={{ color: "var(--text-muted)", fontFamily: "var(--font-mono)", fontSize: 13 }}>Score calculated after run completes…</p>
    </div>
  );
  const base = score?.base_score || 100;
  const bonus = score?.speed_bonus || 0;
  const penalty = score?.efficiency_penalty || 0;
  const total = score?.total_score ?? "—";
  const rows = [
    { label: "Base Score", val: `+${base}`, cls: "neu", barPct: 100, barCls: "base" },
    { label: "Speed Bonus (<5 min)", val: `+${bonus}`, cls: "pos", barPct: bonus / 10 * 100, barCls: "bonus" },
    { label: "Efficiency Penalty", val: `-${penalty}`, cls: penalty > 0 ? "neg" : "neu", barPct: Math.min(penalty / 40 * 100, 100), barCls: "penalty" },
  ];
  return (
    <div className="card">
      <div className="card-header"><h2>🏆 Score Breakdown</h2></div>
      <div className="score-total">{total}</div>
      <div className="score-rows">
        {rows.map((row, i) => (
          <div key={i} className="score-row">
            <span className="score-row-label">{row.label}</span>
            <div className="score-bar-track"><div className={`score-bar-fill ${row.barCls}`} style={{ width: `${row.barPct}%` }} /></div>
            <span className={`score-row-val ${row.cls}`}>{row.val}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── FixesTable ──
export function FixesTable({ fixes }) {
  return (
    <div className="card">
      <div className="card-header"><h2>🔧 Fixes Applied ({fixes.length})</h2></div>
      <div className="fixes-table-wrap">
        <table>
          <thead>
            <tr><th>File</th><th>Bug Type</th><th>Line</th><th>Commit Message</th><th>Status</th></tr>
          </thead>
          <tbody>
            {fixes.map((fix, i) => (
              <tr key={i}>
                <td style={{ color: "var(--accent)" }}>{fix.file}</td>
                <td><span className={`bug-type-badge bug-${fix.bug_type}`}>{fix.bug_type}</span></td>
                <td>{fix.line || "—"}</td>
                <td>{fix.commit_message || fix.fix_applied || "—"}</td>
                <td>{fix.status === "Fixed" ? <span className="status-fixed">✓ Fixed</span> : <span className="status-failed">✗ Failed</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ── CICDTimeline ──
export function CICDTimeline({ runs, maxRetries }) {
  return (
    <div className="card">
      <div className="card-header"><h2>📡 CI/CD Timeline</h2></div>
      <div className="timeline">
        {runs.map((run, i) => {
          const passed = run.status === "PASSED" || run.conclusion === "success";
          const failed = run.status === "FAILED" || run.conclusion === "failure";
          return (
            <div key={i} className="timeline-item">
              <div className={`timeline-dot ${passed ? "passed" : failed ? "failed" : "running"}`} />
              <div className="timeline-content">
                <div className="timeline-header">
                  <span className="timeline-iter">Iteration {run.iteration || i + 1}</span>
                  <StatusBadge status={passed ? "PASSED" : failed ? "FAILED" : "RUNNING"} />
                  <span className="timeline-ts">{run.timestamp ? new Date(run.timestamp).toLocaleTimeString() : "—"}</span>
                </div>
                {run.duration_seconds && <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-muted)" }}>Duration: {run.duration_seconds}s</span>}
              </div>
            </div>
          );
        })}
      </div>
      <p className="timeline-counter">{runs.length} / {maxRetries} retries used</p>
    </div>
  );
}

export default StatusBadge;