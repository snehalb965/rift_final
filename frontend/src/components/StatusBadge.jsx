export default function StatusBadge({ status, large }) {
  const icons = {
    PASSED: "✓", COMPLETED: "✓",
    FAILED: "✗", ERROR: "✗",
    STARTING: "◌", RUNNING: "◌", CLONING: "◌",
    UNKNOWN: "?", TIMEOUT: "⏱",
  };
  return (
    <span className={`badge badge-${status} ${large ? "large" : ""}`}>
      {icons[status] || "●"} {status}
    </span>
  );
}