export default function FixesTable({ fixes }) {
  return (
    <div className="card">
      <div className="card-header"><h2>🔧 Fixes Applied ({fixes.length})</h2></div>
      <div className="fixes-table-wrap">
        <table>
          <thead>
            <tr>
              <th>File</th>
              <th>Bug Type</th>
              <th>Line</th>
              <th>Commit Message</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {fixes.map((fix, i) => (
              <tr key={i}>
                <td style={{ color: "var(--accent)", maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis" }}>
                  {fix.file}
                </td>
                <td>
                  <span className={`bug-type-badge bug-${fix.bug_type}`}>{fix.bug_type}</span>
                </td>
                <td>{fix.line || "—"}</td>
                <td style={{ maxWidth: 260, overflow: "hidden", textOverflow: "ellipsis" }}>
                  {fix.commit_message || fix.fix_applied || "—"}
                </td>
                <td>
                  {fix.status === "Fixed" || fix.status === "fixed"
                    ? <span className="status-fixed">✓ Fixed</span>
                    : <span className="status-failed">✗ Failed</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}