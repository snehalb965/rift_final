import StatusBadge from "./StatusBadge";

export default function RunSummaryCard({ data }) {
  const duration = () => {
    if (!data.started_at || !data.completed_at) return "—";
    const s = (new Date(data.completed_at) - new Date(data.started_at)) / 1000;
    return s < 60 ? `${Math.round(s)}s` : `${Math.floor(s / 60)}m ${Math.round(s % 60)}s`;
  };

  const items = [
    { label: "Repository",        value: data.repo_url,      cls: "mono" },
    { label: "Team",              value: data.team_name || "—" },
    { label: "Leader",            value: data.leader_name || "—" },
    { label: "Branch Created",    value: data.branch_name || "—", cls: "accent mono" },
    { label: "Failures Detected", value: data.total_fixes ?? "—", cls: "big" },
    { label: "Fixes Applied",     value: data.total_fixes ?? "—", cls: "big" },
    { label: "Time Taken",        value: duration(),          cls: "big" },
    { label: "CI/CD Status",      value: <StatusBadge status={data.final_ci_status || data.status || "UNKNOWN"} /> },
    { label: "Run ID",            value: data.run_id || "—",  cls: "mono" },
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