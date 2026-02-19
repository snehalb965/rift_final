export default function ScorePanel({ score, loading }) {
  if (!score && !loading) return (
    <div className="card">
      <div className="card-header"><h2>🏆 Score</h2></div>
      <p style={{ color: "var(--text-muted)", fontFamily: "var(--font-mono)", fontSize: 13 }}>
        Score calculated after run completes…
      </p>
    </div>
  );

  const base    = score?.base_score         || 100;
  const bonus   = score?.speed_bonus        || 0;
  const penalty = score?.efficiency_penalty || 0;
  const total   = score?.total_score        ?? "—";

  const rows = [
    { label: "Base Score",           val: `+${base}`,    cls: "neu", barPct: 100,                          barCls: "base"    },
    { label: "Speed Bonus (<5 min)", val: `+${bonus}`,   cls: "pos", barPct: (bonus / 10) * 100,           barCls: "bonus"   },
    { label: "Efficiency Penalty",   val: `-${penalty}`, cls: penalty > 0 ? "neg" : "neu", barPct: Math.min((penalty / 40) * 100, 100), barCls: "penalty" },
  ];

  return (
    <div className="card">
      <div className="card-header"><h2>🏆 Score Breakdown</h2></div>
      <div className="score-total">{total}</div>
      <div className="score-rows">
        {rows.map((row, i) => (
          <div key={i} className="score-row">
            <span className="score-row-label">{row.label}</span>
            <div className="score-bar-track">
              <div className={`score-bar-fill ${row.barCls}`} style={{ width: `${row.barPct}%` }} />
            </div>
            <span className={`score-row-val ${row.cls}`}>{row.val}</span>
          </div>
        ))}
      </div>
    </div>
  );
}