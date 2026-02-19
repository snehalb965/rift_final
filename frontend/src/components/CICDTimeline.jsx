import StatusBadge from "./StatusBadge";

export default function CICDTimeline({ runs, maxRetries }) {
  const fmt = (ts) => ts ? new Date(ts).toLocaleTimeString() : "—";

  return (
    <div className="card">
      <div className="card-header"><h2>📡 CI/CD Timeline</h2></div>
      <div className="timeline">
        {runs.map((run, i) => {
          const passed = run.status === "PASSED" || run.conclusion === "success";
          const failed = run.status === "FAILED" || run.conclusion === "failure";
          const dotCls = passed ? "passed" : failed ? "failed" : "running";
          return (
            <div key={i} className="timeline-item">
              <div className={`timeline-dot ${dotCls}`} />
              <div className="timeline-content">
                <div className="timeline-header">
                  <span className="timeline-iter">Iteration {run.iteration || i + 1}</span>
                  <StatusBadge status={passed ? "PASSED" : failed ? "FAILED" : "RUNNING"} />
                  <span className="timeline-ts">{fmt(run.timestamp)}</span>
                </div>
                {run.duration_seconds && (
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-muted)" }}>
                    Duration: {run.duration_seconds}s
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
      <p className="timeline-counter">{runs.length} / {maxRetries} retries used</p>
    </div>
  );
}